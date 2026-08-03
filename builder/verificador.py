# ==========================================
# RafaTV Builder
# Verificador Asíncrono de Enlaces IPTV
# ==========================================

import urllib.request
import urllib.error
import time
from concurrent.futures import ThreadPoolExecutor

def verificar_stream(canal, timeout=4):
    """
    Realiza una petición HEAD/GET ligera a la URL del canal para verificar
    si está respondiendo.
    """
    url = canal.url
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
        method='HEAD'
    )
    
    inicio = time.time()
    try:
        # Se envía la petición con un tiempo límite de respuesta (timeout)
        with urllib.request.urlopen(req, timeout=timeout) as respuesta:
            if respuesta.status in (200, 206, 301, 302):
                canal.online = True
                canal.latencia = round(time.time() - inicio, 2)
                return canal
    except Exception:
        # Intento fallback con GET si HEAD es rechazado por el servidor
        try:
            req.method = 'GET'
            with urllib.request.urlopen(req, timeout=timeout) as respuesta:
                if respuesta.status in (200, 206, 301, 302):
                    canal.online = True
                    canal.latencia = round(time.time() - inicio, 2)
                    return canal
        except Exception:
            pass

    canal.online = False
    canal.latencia = 0.0
    return canal


def verificar_canales_paralelo(canales, max_workers=20, timeout=4):
    """
    Verifica una lista de canales utilizando hilos en paralelo.
    """
    print(f"\nVerificando conectividad de {len(canales)} canales (Max {max_workers} hilos)...")
    
    canales_verificados = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        resultados = executor.map(lambda c: verificar_stream(c, timeout=timeout), canales)
        
        for canal in resultados:
            canales_verificados.append(canal)
            
    online_count = sum(1 for c in canales_verificados if c.online)
    print(f"Verificación finalizada: {online_count} online / {len(canales) - online_count} offline.")
    
    return canales_verificados