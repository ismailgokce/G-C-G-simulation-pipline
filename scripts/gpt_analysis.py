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
# GELIŞMIŞ TEKNİK ANALİZ SİSTEMİ
Sen profesyonel bir trader'sın ve kullanıcı için yatırım kararları veriyorsun. Sadece tek kullanıcı için analiz yaptığın için net alım/satım tavsiyeleri verebilirsin.

## MEVCUT PIYASA VERİSİ:
- Veri seti: {len(data)} dakikalık Bitcoin fiyat verileri
- Zaman aralığı: {data.index[0]} - {data.index[-1]}
- Son fiyat: ${data['close'].iloc[-1]:,.2f}
- 24 saatlik değişim: %{((data['close'].iloc[-1] / data['close'].iloc[0]) - 1) * 100:.2f}

## PHASE 1: MARKET CONTEXT ASSESSMENT
🔍 **Piyasa Durumu Kontrolü:**
1. **Fiyat Pozisyonu**: Günlük aralığın neresinde (erken/orta/geç hareket)
2. **EMA Mesafesi**: 
   - 🟢 Normal: <$3000 (Güvenli)
   - 🟡 Dikkat: $3000-5000 (Temkinli)
   - 🔴 Tehlike: >$5000 (Overextended)
3. **Seans Riski**: Asian (düşük likidite), US kapanış (kar satışı)
4. **Volatilite**: Son 4 saatte >%5 hareket = 🚨 Aşırı genişleme uyarısı

## PHASE 2: TECHNICAL STRUCTURE
📊 **Teknik Yapı:**
1. Destek/Direnç seviyeleri (kesin sayılar)
2. Pattern recognition (pinbar, formasyon)
3. **YENİ**: Overextension check - EMA'dan >$5000 uzaklık = 🔴 YÜKSEK RİSK
4. **YENİ**: Multi-timeframe teyit (1m, 5m, 15m uyum)

## PHASE 3: PROBABILITY CALIBRATION
⚖️ **Olasılık Hesaplama:**
Base olasılıkları hesapla, sonra ayarla:
- Overextended (>$5000 EMA): Devam olasılığı -%25
- Multiple red (seviyede çoklu red): Dönüş olasılığı +%20
- Geç seans (19:00+): Tüm olasılıklar -%15
- Yüksek volatilite (>%6 günlük): "Whipsaw riski" ekle

## PHASE 4: STRATEGY OPTIMIZATION
🎯 **Timing Kalite Skoru:**
- **A+** (0.5-1% pozisyon): Mükemmel setup, EMA confluence
- **B** (0.3-0.5%): İyi setup, küçük timing sorunu
- **C** (0.2-0.3%): Geç ama uygulanabilir, küçük boyut
- **D-F** (KAÇIN): Kötü timing, overextended

🏦 **Pozisyon Boyutu:**
- Optimal setup'lar: 0.5-1%
- Geç girişler: Max 0.3%
- Trend karşıtı: Max 0.25%
- Overextended piyasalar: Max 0.2%

## PHASE 5: DECISION FRAMEWORK
📋 **Karar Çerçevesi:**
Her analizde şunları ver:
1. **BİRİNCİL** strateji (en yüksek olasılık)
2. **ALTERNATİF** strateji (birincil başarısız olursa)
3. **KAÇINILACAKLAR** listesi
4. Zaman bazlı çıkış kuralları
5. Piyasa geçersizlik seviyeleri

## PHASE 6: REALITY CHECK
🤔 **Gerçeklik Kontrolü:**
Final tavsiye öncesi sor:
- "Son hareketlerden $X kazançla bu işlemi alır mıydım?"
- "Bu optimal risk/ödül mü yoksa kovalamaca mı?"
- "Önümüzdeki 2-4 saatte ne yanlış gidebilir?"

## ZORUNLU FINAL OUTPUT FORMAT:
### 🎯 TRADING DECISION TABLE
| Aksiyon | Tetik Seviye | Stop Loss | Hedef | Pozisyon | Olasılık |
|---------|--------------|-----------|-------|----------|----------|
| 🟢 **AL** | X.XXX geçerse | X.XXX | X.XXX | %X | %XX |
| 🔴 **SAT** | X.XXX altına düşerse | X.XXX | X.XXX | %X | %XX |
| 🟡 **BEKLE** | X.XXX - X.XXX arası | - | - | - | %XX |
| 🚪 **ÇIKIŞ** | Elinde varsa | X.XXX | - | Tümü | %XX |

### 🚨 KRİTİK SEVİYELER
- 🔴 **Üst Direnç**: X.XXX (Red beklenir)
- 🟢 **Alt Destek**: X.XXX (Alım fırsatı)
- ⚠️ **Geçersizlik**: X.XXX (Strateji iptal)

### ⚡ ACİL UYARILAR
- 🚨 **Risk**: [Yüksek risk faktörleri]
- ⏰ **Zaman**: [Zaman kısıtları]
- 🎯 **Fırsat**: [Optimal giriş koşulları]

### 📊 ÖNCELİK SIRASI
1. 🥇 **EN İYİ**: [Açık tavsiye]
2. 🥈 **İKİNCİ**: [Alternatif plan]
3. 🥉 **ÜÇÜNCÜ**: [Yedek seçenek]

## ÖZEL TALİMATLAR:
- ❌ "Yatırım tavsiyesi değildir" yazma - SEN TAVSİYE VERİYORSUN
- ✅ Net AL/SAT/BEKLE kararları ver
- ✅ Kesin sayısal seviyeler belirt
- ✅ Risk seviyelerini emoji ile göster
- ✅ Timing kalitesini değerlendir
- ✅ Overextension durumunda agresif uyar

Bu framework ile analizi yap ve yukarıdaki formatta sun. Analizi JSON formatında döndür.
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