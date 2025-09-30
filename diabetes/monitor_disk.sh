#!/bin/bash

# Script para monitorar espaço em disco durante a execução dos trials
# Executa em background e limpa arquivos quando necessário

LOGFILE="diabetes/disk_monitor.log"
CLEANUP_THRESHOLD=90  # Limpa quando uso > 90%
STOP_THRESHOLD=95     # Para execução quando uso > 95%

echo "$(date): Iniciando monitoramento de disco..." >> "$LOGFILE"

while true; do
    # Verifica uso do disco
    USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    
    if [ "$USAGE" -gt $CLEANUP_THRESHOLD ]; then
        echo "$(date): Uso de disco alto: ${USAGE}%. Iniciando limpeza..." >> "$LOGFILE"
        
        # Limpeza agressiva
        find /tmp -type f -mmin +5 -delete 2>/dev/null || true
        find /tmp -name "*.tmp" -delete 2>/dev/null || true
        find /tmp -name ".tmp*" -delete 2>/dev/null || true
        
        # Limpa cache do pip
        if [ -d "$HOME/.cache/pip" ]; then
            rm -rf "$HOME/.cache/pip/wheels" 2>/dev/null || true
        fi
        
        # Limpa arquivos Python temporários
        find /tmp -name "*python*" -type f -mmin +10 -delete 2>/dev/null || true
        
        # Verifica novamente
        NEW_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
        echo "$(date): Uso após limpeza: ${NEW_USAGE}%" >> "$LOGFILE"
        
        if [ "$NEW_USAGE" -gt $STOP_THRESHOLD ]; then
            echo "$(date): ALERTA: Uso crítico de disco (${NEW_USAGE}%)!" >> "$LOGFILE"
            # Pode enviar sinal para parar execução se necessário
            # pkill -f "run_model.py" 2>/dev/null || true
        fi
    fi
    
    # Aguarda 30 segundos antes da próxima verificação
    sleep 30
done
