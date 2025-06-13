#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📋 GPT-Claude Final Karşılaştırma Script
LATU Trading System - Final Comparison Pipeline
"""

import os
import argparse
import json
import requests
from datetime import datetime
import openai

def final_comparison_analysis(symbol, gpt_result, claude_result):
    """📋 GPT-Claude karşılaştırma ve final karar"""
    
    # OpenAI API ayarları
    openai.api_key = os.environ['OPENAI_API_KEY']
    
    # Final karşılaştırma prompt
    prompt = f"""
Sen bir baş analist olarak GPT ve Claude'un {symbol} analizlerini karşılaştır ve final bir karar ver.

🚀 GPT ANALİZİ:
{gpt_result}

🤖 CLAUDE ANALİZİ:
{claude_result}

Şu formatla bir karşılaştırma tablosu ve final karar hazırla:

📊 **GPT-CLAUDE KARŞILAŞTIRMA TABLOSU - {symbol.upper()}**

| **KRİTER** | **GPT ANALİZİ** | **CLAUDE ANALİZİ** | **FARK/YORUM** |
|------------|-----------------|-------------------|----------------|
| **Karar** | [GPT kararı] | [Claude kararı] | [Hangi daha iyi] |
| **Risk Yaklaşımı** | [GPT risk] | [Claude risk] | [Karşılaştırma] |
| **Entry Seviyesi** | [GPT entry] | [Claude entry] | [Fark analizi] |
| **Stop Loss** | [GPT stop] | [Claude stop] | [Hangisi daha güvenli] |
| **Hedef Seviye** | [GPT hedef] | [Claude hedef] | [Gerçekçilik] |
| **Zaman Horizonu** | [GPT zaman] | [Claude zaman] | [Hangisi daha uygun] |
| **Güvenilirlik** | [GPT %] | [Claude %] | [Karşılaştırma] |

**🧠 ANALİZ FARKLILIKARI:**
- **Hız vs Detay**: [GPT hızlı, Claude detaylı karşılaştırması]
- **Risk Yönetimi**: [Hangisi daha konservatif]
- **Teknik Analiz**: [Derinlik karşılaştırması]
- **Pratiklik**: [Hangisi daha uygulanabilir]

**⚖️ GÜÇLÜ VE ZAYIF YANLAR:**

**GPT'nin Güçlü Yanları:**
- [Hızlı karar verme]
- [Net pozisyon alma]
- [Momentum yakalama]

**GPT'nin Zayıf Yanları:**
- [Risk yönetimi eksikliği]
- [Detay eksikliği]

**Claude'un Güçlü Yanları:**
- [Detaylı teknik analiz]
- [Risk yönetimi]
- [Çoklu senaryo]

**Claude'un Zayıf Yanları:**
- [Aşırı temkinli]
- [Karmaşık strateji]

**🏆 FİNAL KARAR:**

**Önerilen Strateji:** [AL/SAT/BEKLE]
**Güvenilirlik:** [%X]
**Pozisyon Büyüklüğü:** [%X]
**Entry:** $[X]
**Stop Loss:** $[X]  
**Take Profit:** $[X]

**📋 UYGULAMA PLANI:**
1. [Adım 1]
2. [Adım 2]
3. [Adım 3]

**⚡ HIZLI AKSİYON:**
[Tek cümlelik actionable öneri]

**💡 SONUÇ:**
[GPT ve Claude'un en iyi yanlarını birleştiren final değerlendirme]

Bu karşılaştırmada:
1. Her iki analizin güçlü yanlarını değerlendir
2. Risk-return dengesini optimize et
3. Pratik ve uygulanabilir bir strateji sun
4. Net bir karar ver, belirsizlik bırakma
    """
    
    try:
        print(f"📋 Final karşılaştırma analizi başlatılıyor: {symbol}")
        
        # OpenAI API çağrısı
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "Sen bir baş trading analistisin. Farklı analiz kaynaklarını karşılaştırıp en optimal stratejiyi belirlersin. Tablolar, karşılaştırmalar ve net kararlar verirsin."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=1200,
            temperature=0.8
        )
        
        final_result = response.choices[0].message.content.strip()
        
        # Sonucu results klasörüne kaydet
        os.makedirs('results', exist_ok=True)
        result_file = f'results/final_{symbol}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(final_result)
        
        # Tüm analizi birleştir
        complete_analysis = f"""
=== LATU TRADING SYSTEM - COMPLETE ANALYSIS ===
Sembol: {symbol}
Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

{gpt_result}

---

{claude_result}

---

{final_result}

=== PIPELINE TAMAMLANDI ===
        """
        
        complete_file = f'results/complete_{symbol}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        with open(complete_file, 'w', encoding='utf-8') as f:
            f.write(complete_analysis)
        
        print(f"✅ Final analiz tamamlandı: {result_file}")
        print(f"✅ Komplet analiz kaydedildi: {complete_file}")
        
        return final_result
        
    except Exception as e:
        print(f"❌ Final analiz hatası: {e}")
        return None

def send_final_result_to_dashboard(symbol, final_result, webhook_url):
    """📤 Dashboard'a final sonuç gönder"""
    
    try:
        payload = {
            'symbol': symbol,
            'stage': 'final-completed',
            'result': final_result,
            'timestamp': datetime.now().isoformat(),
            'pipeline_status': 'completed'
        }
        
        response = requests.post(webhook_url, json=payload, timeout=15)
        
        if response.status_code == 200:
            print("✅ Dashboard'a final sonuç gönderildi")
        else:
            print(f"⚠️ Dashboard gönderim hatası: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Dashboard gönderim hatası: {e}")

def main():
    """📋 Ana fonksiyon"""
    
    parser = argparse.ArgumentParser(description='GPT-Claude Final Karşılaştırma Script')
    parser.add_argument('--symbol', required=True, help='Trading sembolü')
    parser.add_argument('--gpt-result', required=True, help='GPT analiz sonucu')
    parser.add_argument('--claude-result', required=True, help='Claude analiz sonucu')
    parser.add_argument('--webhook-url', required=True, help='Dashboard webhook URL')
    
    args = parser.parse_args()
    
    print("📋 LATU Final Comparison Pipeline Başlatıldı")
    print(f"📊 Analiz edilen sembol: {args.symbol}")
    print(f"📄 GPT sonucu: {len(args.gpt_result)} karakter")
    print(f"📄 Claude sonucu: {len(args.claude_result)} karakter")
    
    # Final karşılaştırma analizini yap
    final_result = final_comparison_analysis(args.symbol, args.gpt_result, args.claude_result)
    
    if final_result:
        # Dashboard'a final sonucu gönder
        send_final_result_to_dashboard(args.symbol, final_result, args.webhook_url)
        
        print("🎯 PIPELINE BAŞARIYLA TAMAMLANDI!")
        print("📊 Tüm analizler Dashboard'a gönderildi")
        print("✅ GPT → Claude → Final karşılaştırması hazır")
        
    else:
        print("❌ Final analiz başarısız!")
        exit(1)

if __name__ == "__main__":
    main()