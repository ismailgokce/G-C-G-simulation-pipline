#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Claude Detaylı Teknik Analiz Script
LATU Trading System - Claude Analysis Pipeline
"""

import os
import argparse
import json
import requests
from datetime import datetime
import anthropic

def claude_detailed_analysis(symbol, gpt_result):
    """🤖 Claude detaylı teknik analiz fonksiyonu"""
    
    # Anthropic API ayarları
    client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
    
    # Claude'a gönderilecek prompt
    prompt = f"""
GPT'nin ilk hızlı analizi şu şekilde:

{gpt_result}

Sen Claude olarak, bu GPT analizini temel alarak çok daha detaylı ve profesyonel bir teknik analiz yap. 

MUTLAKA şu formatı kullan (başka format kullanma):

🤖 Claude Teknik Analiz - {symbol.upper()}

📊 **GPT İlk Değerlendirmesi Alındı**
- GPT Kararı: [GPT'nin kararını buraya yaz]
- İlk momentum: [GPT'nin bahsettiği değişim %'sini yaz]

🧠 **Claude Derinlemesine Analiz:**

**Teknik Göstergeler:**
- RSI: [30-70 arası bir değer hesapla ve yorumla]
- MACD: [Pozitif/Negatif momentum belirle]
- Volume Profil: [Yüksek/Normal/Düşük volume analiz et]
- Bollinger Bands: [Genişlik/daralma durumu]

**Fiyat Seviyeleri:**
- Destek: $[hesapla ve yakın seviye belirle]
- Direnç: $[hesapla ve yakın seviye belirle]  
- Entry: $[optimal giriş noktası belirle]
- Stop Loss: $[risk yönetimi için stop seviyesi]

**Claude Risk Değerlendirmesi:**
- Risk Seviyesi: [Yüksek/Orta/Düşük - detaylı gerekçe ile]
- R/R Oranı: [1:1.5 ile 1:3 arası gerçekçi oran]
- Güvenilirlik Oranı: [%60-90 arası]
- Position Size Önerisi: [%0.5-2 arası]

**Market Psychology & Sentiment:**
- Piyasa Duygusu: [Fear/Greed/Neutral analizi]
- Volume-Price İlişkisi: [Divergence/Convergence]
- Trend Gücü: [Güçlü/Orta/Zayıf]

**Claude Kararı:** [KOŞULLU AL/KOŞULLU SAT/BEKLE]

**Stratejik Notlar:**
- [Önemli seviyeler ve dikkat edilmesi gerekenler]
- [Risk faktörleri]
- [Alternatif senaryolar]

Bu analizi yaparken:
1. GPT'den daha temkinli ve konservatif ol
2. Risk yönetimini her zaman ön planda tut
3. Teknik detaylara derinlemesine odaklan
4. Gerçekçi ve uygulanabilir hedefler koy
5. Multiple timeframe perspektifi kullan
    """
    
    try:
        print(f"🤖 Claude detaylı analizi başlatılıyor: {symbol}")
        
        # Anthropic API çağrısı
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        
        claude_result = response.content[0].text.strip()
        
        # Sonucu results klasörüne kaydet
        os.makedirs('results', exist_ok=True)
        result_file = f'results/claude_{symbol}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(claude_result)
        
        print(f"✅ Claude analizi tamamlandı ve kaydedildi: {result_file}")
        return claude_result
        
    except Exception as e:
        print(f"❌ Claude API hatası: {e}")
        return None

def trigger_final_stage(symbol, gpt_result, claude_result, webhook_url):
    """🔄 Final karşılaştırma aşamasını tetikle"""
    
    try:
        # GitHub'a final aşama için webhook gönder
        github_payload = {
            'event_type': 'analysis-request',
            'client_payload': {
                'symbol': symbol,
                'stage': 'final-comparison',
                'gpt_result': gpt_result,
                'claude_result': claude_result,
                'webhook_url': webhook_url,
                'timestamp': datetime.now().isoformat()
            }
        }
        
        headers = {
            'Authorization': f'token {os.environ["GITHUB_TOKEN"]}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        # GitHub repo bilgileri
        repo_info = os.environ.get('GITHUB_REPOSITORY', 'user/G-C-G-simulation-pipline')
        github_url = f'https://api.github.com/repos/{repo_info}/dispatches'
        
        response = requests.post(github_url, json=github_payload, headers=headers)
        
        if response.status_code == 204:
            print("✅ Final karşılaştırma aşaması tetiklendi")
        else:
            print(f"⚠️ Final tetikleme hatası: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Final tetikleme hatası: {e}")

def send_result_to_dashboard(symbol, stage, result, webhook_url):
    """📤 Dashboard'a sonuç gönder"""
    
    try:
        payload = {
            'symbol': symbol,
            'stage': stage,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Dashboard'a Claude sonucu gönderildi")
        else:
            print(f"⚠️ Dashboard gönderim hatası: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Dashboard gönderim hatası: {e}")

def main():
    """🤖 Ana fonksiyon"""
    
    parser = argparse.ArgumentParser(description='Claude Detaylı Analiz Script')
    parser.add_argument('--symbol', required=True, help='Trading sembolü')
    parser.add_argument('--gpt-result', required=True, help='GPT analiz sonucu')
    parser.add_argument('--webhook-url', required=True, help='Dashboard webhook URL')
    
    args = parser.parse_args()
    
    print("🤖 LATU Claude Analysis Pipeline Başlatıldı")
    print(f"📊 Analiz edilen sembol: {args.symbol}")
    print(f"📄 GPT sonucu alındı: {len(args.gpt_result)} karakter")
    
    # Claude detaylı analizini yap
    claude_result = claude_detailed_analysis(args.symbol, args.gpt_result)
    
    if claude_result:
        # Dashboard'a Claude sonucunu gönder
        send_result_to_dashboard(args.symbol, 'claude-completed', claude_result, args.webhook_url)
        
        # Final karşılaştırma aşamasını tetikle
        trigger_final_stage(args.symbol, args.gpt_result, claude_result, args.webhook_url)
        
        print("🎯 Claude aşaması başarıyla tamamlandı!")
        
    else:
        print("❌ Claude analizi başarısız!")
        exit(1)

if __name__ == "__main__":
    main()