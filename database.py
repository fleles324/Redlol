import os
import re
import config
from supabase import create_client, Client

class Database:
    def __init__(self):
        # As credenciais devem ser configuradas no config.py
        self.url: str = config.SUPABASE_URL
        self.key: str = config.SUPABASE_KEY
        if self.url and self.key:
            self.supabase: Client = create_client(self.url, self.key)
        else:
            print("[ERRO] Supabase URL ou Key não configurados no config.py!")
            self.supabase = None

    # --- Operações de Usuário ---
    def update_user(self, user_id, username=None, first_name=None):
        if not self.supabase: return
        data = {"user_id": user_id, "last_seen": "now()"}
        if username: data["username"] = username.lower()
        if first_name: data["first_name"] = first_name
        self.supabase.table("users").upsert(data).execute()

    def increment_user_msgs(self, user_id):
        if not self.supabase: return
        res = self.supabase.table("users").select("msg_count").eq("user_id", user_id).execute()
        if res.data:
            new_count = (res.data[0]['msg_count'] or 0) + 1
            self.supabase.table("users").update({"msg_count": new_count}).eq("user_id", user_id).execute()

    def get_user_ranking(self, limit=10):
        if not self.supabase: return []
        res = self.supabase.table("users").select("username, first_name, msg_count").order("msg_count", desc=True).limit(limit).execute()
        return res.data

    # --- Operações de Chat ---
    def get_chat_settings(self, chat_id):
        if not self.supabase: return {}
        res = self.supabase.table("chat_settings").select("*").eq("chat_id", chat_id).execute()
        if res.data:
            return res.data[0]
        else:
            default_data = {"chat_id": chat_id, "language": "pt_BR"}
            self.supabase.table("chat_settings").insert(default_data).execute()
            return default_data

    def update_chat_setting(self, chat_id, column, value):
        if not self.supabase: return
        self.supabase.table("chat_settings").update({column: value}).eq("chat_id", chat_id).execute()

    # --- Operações de Suporte & Avaliação ---
    def add_rating(self, user_id, atendente_id, score):
        if not self.supabase: return
        self.supabase.table("bot_stats").upsert({
            "stat_name": f"rating:{atendente_id}:{user_id}",
            "stat_value": score
        }).execute()

    def get_top_atendentes(self, limit=5):
        if not self.supabase: return []
        # Esta é uma simulação, em um banco real usaríamos agregação SQL
        res = self.supabase.table("bot_stats").select("*").like("stat_name", "rating:%").execute()
        ratings = {}
        for r in res.data:
            atendente_id = int(r['stat_name'].split(':')[1])
            if atendente_id not in ratings:
                ratings[atendente_id] = []
            ratings[atendente_id].append(r['stat_value'])
        
        result = []
        for aid, scores in ratings.items():
            result.append({
                "atendente_id": aid,
                "average": sum(scores) / len(scores),
                "count": len(scores)
            })
        return sorted(result, key=lambda x: x['average'], reverse=True)[:limit]

    # --- Operações de Extras & Respostas Rápidas ---
    def set_quick_reply(self, key, text):
        if not self.supabase: return
        self.supabase.table("chat_extras").upsert({
            "chat_id": 0,
            "command": f"qr:{key}",
            "response": text
        }).execute()

    def get_quick_reply(self, key):
        if not self.supabase: return None
        res = self.supabase.table("chat_extras").select("response").eq("chat_id", 0).eq("command", f"qr:{key}").execute()
        if res.data:
            return res.data[0]['response']
        return None

    def get_all_quick_replies(self):
        if not self.supabase: return []
        res = self.supabase.table("chat_extras").select("command, response").eq("chat_id", 0).like("command", "qr:%").execute()
        replies = []
        for item in res.data:
            replies.append({
                "key": item['command'].replace("qr:", ""),
                "response": item['response']
            })
        return replies

    def search_faq(self, query):
        """Busca no FAQ por palavras-chave ou categoria com maior inteligência"""
        if not self.supabase: return None
        
        # Busca todas as FAQs ativas
        res = self.supabase.table("faqs").select("*").eq("active", True).execute()
        
        if not res.data:
            return None
            
        query = query.lower().strip()
        # Remove pontuação básica para melhorar a busca
        clean_query = re.sub(r'[!?.,]', '', query)
        query_words = set(clean_query.split())
        
        best_match = None
        highest_score = 0
        
        for faq in res.data:
            score = 0
            keywords = [k.lower().strip() for k in (faq.get('keywords') or [])]
            category = (faq.get('category') or "").lower().strip()
            topic_id = (faq.get('topic_id') or "").lower().strip()
            answer = (faq.get('answer') or "").lower()
            
            # 0. Verificação de topic_id dentro da frase (Peso Máximo)
            if topic_id and topic_id in clean_query:
                score += 20
            
            # 1. Correspondência exata na categoria (Peso alto)
            if clean_query == category:
                score += 10
            
            # 2. Correspondência exata em alguma keyword (Peso alto)
            if any(clean_query == k for k in keywords):
                score += 8
            
            # 3. Quantidade de palavras da pergunta que estão nas keywords (Peso médio)
            matches = sum(1 for word in query_words if any(word in k or k in word for k in keywords))
            score += matches * 2
            
            # 4. Verificação na categoria (Peso baixo)
            if any(word in category for word in query_words):
                score += 1
                
            # 5. Verificação na resposta (Peso muito baixo - apenas desempate)
            if any(word in answer for word in query_words):
                score += 0.5
            
            if score > highest_score:
                highest_score = score
                best_match = faq
        
        # Só retorna se a pontuação mínima de relevância for atingida
        return best_match if highest_score >= 2 else None

    # --- Operações de Tickets Persistentes ---
    def create_ticket(self, thread_id, user_id, user_name, lang='pt_BR'):
        """Cria ou atualiza um ticket na fila"""
        if not self.supabase: return
        try:
            # Verifica se já existe um ticket pendente para este usuário
            existing = self.supabase.table("tickets").select("*").eq("user_id", user_id).eq("status", "pending").execute()
            if existing.data:
                # Apenas atualiza o thread_id e status se for o caso de aceitar
                ticket_id = existing.data[0]['id']
                self.supabase.table("tickets").update({
                    "thread_id": thread_id,
                    "status": "open",
                    "language": lang
                }).eq("id", ticket_id).execute()
            else:
                # Cria novo ticket pendente (fila)
                self.supabase.table("tickets").insert({
                    "user_id": user_id,
                    "user_name": user_name,
                    "thread_id": thread_id,
                    "status": "pending",
                    "language": lang
                }).execute()
        except Exception as e:
            print(f"[ERRO] database.create_ticket: {e}")

    def get_queue_position(self, user_id):
        """Retorna a posição do usuário na fila de espera"""
        if not self.supabase: return 0
        try:
            # Conta quantos tickets pendentes foram criados antes do deste usuário
            user_ticket = self.supabase.table("tickets").select("id", "created_at").eq("user_id", user_id).eq("status", "pending").execute()
            if not user_ticket.data: return 0
            
            created_at = user_ticket.data[0]['created_at']
            res = self.supabase.table("tickets").select("id", count="exact").eq("status", "pending").lt("created_at", created_at).execute()
            return (res.count or 0) + 1
        except:
            return 0

    def accept_ticket(self, user_id, staff_id, staff_name, thread_id):
        """Staff aceita o ticket da fila"""
        if not self.supabase: return
        try:
            self.supabase.table("tickets").update({
                "status": "open",
                "staff_id": staff_id,
                "staff_name": staff_name,
                "thread_id": thread_id
            }).eq("user_id", user_id).eq("status", "pending").execute()
        except:
            pass

    def get_ticket_by_user(self, user_id):
        """Busca ticket ativo (pendente ou aberto) de um usuário"""
        if not self.supabase: return None
        try:
            res = self.supabase.table("tickets").select("*").eq("user_id", user_id).neq("status", "closed").execute()
            return res.data[0] if res.data else None
        except:
            return None

    def get_ticket_by_thread(self, thread_id):
        """Busca ticket ativo vinculado a um tópico"""
        if not self.supabase: return None
        try:
            res = self.supabase.table("tickets").select("*").eq("thread_id", thread_id).eq("status", "open").execute()
            return res.data[0] if res.data else None
        except:
            return None

    def close_ticket(self, thread_id, user_id):
        """Fecha o ticket no banco"""
        if not self.supabase: return
        try:
            self.supabase.table("tickets").update({
                "status": "closed",
                "closed_at": "now()"
            }).eq("user_id", user_id).neq("status", "closed").execute()
        except:
            pass

    def get_staff_ranking(self):
        """Calcula o ranking Top 10 de atendentes com múltiplas métricas"""
        if not self.supabase: return []
        try:
            # Busca todos os ratings
            res = self.supabase.table("ratings").select("*").execute()
            if not res.data: return []
            
            # Agrupa por atendente
            staff_data = {}
            for r in res.data:
                s_id = r.get('staff_id')
                if not s_id: continue
                
                if s_id not in staff_data:
                    staff_data[s_id] = {
                        "name": r.get('staff_name', 'Atendente'),
                        "csat_total": 0,
                        "nps_total": 0,
                        "frt_total": 0,
                        "fcr_total": 0,
                        "aht_total": 0,
                        "count": 0
                    }
                
                sd = staff_data[s_id]
                sd['csat_total'] += (r.get('score') or 0) * 2 # Escala 1-5 para 1-10
                sd['nps_total'] += (r.get('nps_score') or 0)
                sd['frt_total'] += (r.get('frt_seconds') or 60)
                sd['fcr_total'] += 1 if r.get('fcr') else 0
                sd['aht_total'] += (r.get('aht_seconds') or 300)
                sd['count'] += 1
            
            # Calcula as médias
            ranking = []
            for s_id, data in staff_data.items():
                count = data['count']
                csat = round(data['csat_total'] / count, 1)
                nps = round((data['nps_total'] / count) * 10, 0) # Simplificado para +NPS
                frt = int(data['frt_total'] / count)
                fcr = round((data['fcr_total'] / count) * 100, 1)
                aht = round((data['aht_total'] / count) / 60, 1)
                
                # Média Geral (Peso maior para CSAT e FCR)
                media_geral = round((csat * 10 + nps + fcr) / 3, 1)
                
                ranking.append({
                    "name": data['name'],
                    "csat": csat,
                    "nps": int(nps),
                    "frt": f"{frt}s",
                    "fcr": f"{fcr}%",
                    "aht": f"{aht}m",
                    "media": media_geral
                })
            
            # Ordena pela média geral decrescente
            ranking.sort(key=lambda x: x['media'], reverse=True)
            return ranking[:10]
        except Exception as e:
            print(f"[ERRO] database.get_staff_ranking: {e}")
            return []
    def set_last_ranking_msg(self, message_id):
        """Salva o ID da última mensagem de ranking postada"""
        if not self.supabase: return
        self.supabase.table("bot_stats").upsert({
            "stat_name": "last_ranking_message_id",
            "stat_value": message_id
        }).execute()

    def get_last_ranking_msg(self):
        """Busca o ID da última mensagem de ranking postada"""
        if not self.supabase: return None
        res = self.supabase.table("bot_stats").select("stat_value").eq("stat_name", "last_ranking_message_id").execute()
        return res.data[0]['stat_value'] if res.data else None

    # --- Operações de Língua do Usuário ---
    def set_user_lang(self, user_id, lang):
        if not self.supabase: return
        # Salva o idioma na tabela chat_settings usando o user_id como chat_id (pois no privado são iguais)
        self.supabase.table("chat_settings").upsert({
            "chat_id": user_id,
            "language": lang
        }).execute()

    def get_user_lang(self, user_id):
        if not self.supabase: return None
        res = self.supabase.table("chat_settings").select("language").eq("chat_id", user_id).execute()
        if res.data:
            return res.data[0]['language']
        return None

    def increment_stat(self, stat_name):
        if not self.supabase: return
        res = self.supabase.table("bot_stats").select("stat_value").eq("stat_name", stat_name).execute()
        if res.data:
            new_val = (res.data[0]['stat_value'] or 0) + 1
            self.supabase.table("bot_stats").update({"stat_value": new_val}).eq("stat_name", stat_name).execute()
        else:
            self.supabase.table("bot_stats").insert({"stat_name": stat_name, "stat_value": 1}).execute()

db = Database()
