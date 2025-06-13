#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 GPT İlk Hızlı Analiz Script
LATU Trading System - GPT Analysis Pipeline
"""

import os
import argparse
import json
import requests
from datetime import datetime
import openai

def gpt_first_analysis(symbol, price, change, volume):
    """🚀 GPT ilk hızlı analiz fonksiyonu"""
    
    # OpenAI API ayarları
    openai.api_key = os.environ['OPENAI_API_KEY']
    
    # GPT'ye gönderilecek prompt
    prompt = f"""
Sen profesyonel bir trading analisti olarak {symbol} enstrümanı için HIZLI bir ilk değerlendirme yap.

📊 GÜNCEL MARKET VERİSİ:
- Sembol: {symbol}
- Fiyat: ${price}
- Değişim: {change}%
- Volume: {volume:,.0f}

Tam olarak şu formatla cevap ver (başka hiçbir şey ekleme):

📍 Hazırlayan AI: GPT 🕒 {datetime.now().strftime('%d.%m.%Y - %H:%M')} - Analiz No: 001

🔠 {symbol.upper()} - HIZLI DEĞERLENDİRME

🟩 Fiyat ${price} seviyesinde {'+' if float(change) > 0 else ''}{change}% hareket

📊 **İlk Değerlendirme:**
* **Momentum**: [Pozitif/Negatif değerlendir]
* **Volume**: {volume:,.0f} - [Yüksek/Normal/Düşük]
* **Trend**: [Yükseliş/Düşüş/Yatay trendini belirle]

📉 **Teknik Durum:**
* Fiyat hareketi: [değerlendir]
* Volatilite: [değerlendir]
* Piyasa sentiment: [değerlendir]

🔔 **GPT İlk Karar**: [AL/SAT/BEKLE - sadece bu 3'ünden birini seç]

⏰ **Süreç**: Claude'a detaylı teknik analiz için gönderiliyor...
    """
    
    try:
        print(f"🚀 GPT analizi başlatılıyor: {symbol}")
        
        # OpenAI API çağrısı
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "Sen profesyonel bir trading analistisin. Kısa, net ve actionable analizler yaparsın. Sadece istenen formatla cevap verirsin."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=600,
            temperature=0.7
        )
        
        gpt_result = response.choices[0].message.content.strip()
        
        # Sonucu results klasörüne kaydet
        os.makedirs('results', exist_ok=True)
        result_file = f'results/gpt_{symbol}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(gpt_result)
        
        print(f"✅ GPT analizi tamamlandı ve kaydedildi: {result_file}")
        return gpt_result
        
    except Exception as e:
        print(f"❌ GPT API hatası: {e}")
        return None

def trigger_claude_stage(symbol, gpt_result, webhook_url):
    """🔄 Claude aşamasını tetikle"""
    
    try:
        # GitHub'a Claude aşaması için webhook gönder
        github_payload = {
            'event_type': 'analysis-request',
            'client_payload': {
                'symbol': symbol,
                'stage': 'claude-detailed',
                'gpt_result': gpt_result,
                'webhook_url': webhook_url,
                'timestamp': datetime.now().isoformat()
            }
        }
        
        headers = {
            'Authorization': f'token {os.environ["GITHUB_TOKEN"]}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        # GitHub repo bilgileri (environment'dan al)
        repo_info = os.environ.get('GITHUB_REPOSITORY', 'user/G-C-G-simulation-pipline')
        github_url = f'https://api.github.com/repos/{repo_info}/dispatches'
        
        response = requests.post(github_url, json=github_payload, headers=headers)
        
        if response.status_code == 204:
            print("✅ Claude aşaması tetiklendi")
        else:
            print(f"⚠️ Claude tetikleme hatası: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Claude tetikleme hatası: {e}")

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
            print("✅ Dashboard'a sonuç gönderildi")
        else:
            print(f"⚠️ Dashboard gönderim hatası: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Dashboard gönderim hatası: {e}")

def main():
    """🚀 Ana fonksiyon"""
    
    parser = argparse.ArgumentParser(description='GPT İlk Analiz Script')
    parser.add_argument('--symbol', required=True, help='Trading sembolü')
    parser.add_argument('--price', required=True, type=float, help='Güncel fiyat')
    parser.add_argument('--change', required=True, type=float, help='Değişim yüzdesi')
    parser.add_argument('--volume', required=True, type=float, help='Volume')
    parser.add_argument('--webhook-url', required=True, help='Dashboard webhook URL')
    
    args = parser.parse_args()
    
    print("🚀 LATU GPT Analysis Pipeline Başlatıldı")
    print(f"📊 Analiz edilen sembol: {args.symbol}")
    print(f"💰 Fiyat: ${args.price}")
    print(f"📈 Değişim: {args.change}%")
    print(f"📊 Volume: {args.volume:,.0f}")
    
    # GPT analizini yap
    gpt_result = gpt_first_analysis(args.symbol, args.price, args.change, args.volume)
    
    if gpt_result:
        # Dashboard'a GPT sonucunu gönder
        send_result_to_dashboard(args.symbol, 'gpt-completed', gpt_result, args.webhook_url)
        
        # Claude aşamasını tetikle
        trigger_claude_stage(args.symbol, gpt_result, args.webhook_url)
        
        print("🎯 GPT aşaması başarıyla tamamlandı!")
        
    else:
        print("❌ GPT analizi başarısız!")
        exit(1)

if __name__ == "__main__":
    main()