#!/bin/bash

# Script para executar o modelo de diabetes com diferentes valores de trial
# Executa o run_model.py com valores de trial de 0 a 49

echo "Iniciando execução dos trials..."

# Verifica se o arquivo run_model.py existe
if [ ! -f "diabetes/run_model.py" ]; then
    echo "Erro: Arquivo diabetes/run_model.py não encontrado!"
    exit 1
fi

# Inicia monitoramento de disco em background
if [ -f "diabetes/monitor_disk.sh" ]; then
    echo "Iniciando monitoramento de disco em background..."
    ./diabetes/monitor_disk.sh &
    MONITOR_PID=$!
    echo "Monitor de disco iniciado (PID: $MONITOR_PID)"
fi

# Função para verificar espaço em disco
check_disk_space() {
    local usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ $usage -gt 85 ]; then
        echo "Aviso: Espaço em disco baixo ($usage% usado). Limpando arquivos temporários..."
        # Limpa arquivos temporários antigos de forma mais agressiva
        find /tmp -name ".tmp*" -type f -exec rm -f {} \; 2>/dev/null || true
        find /tmp -name "tmp*" -type f -exec rm -f {} \; 2>/dev/null || true
        find /tmp -name "*.tmp" -type f -exec rm -f {} \; 2>/dev/null || true
        find /tmp -type f -name "*python*" -mmin +30 -exec rm -f {} \; 2>/dev/null || true

        # Limpa cache do pip se existir
        if [ -d "$HOME/.cache/pip" ]; then
            rm -rf "$HOME/.cache/pip/wheels" 2>/dev/null || true
        fi

        # Limpa arquivos de log antigos
        find /var/log -name "*.log.*" -mtime +1 -exec sudo rm -f {} \; 2>/dev/null || true

        # Verifica novamente
        local new_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
        echo "Espaço em disco após limpeza: $new_usage% usado"
        if [ $new_usage -gt 92 ]; then
            echo "Erro: Espaço em disco ainda muito baixo ($new_usage%). Parando execução."
            return 1
        fi
    fi
    return 0
}

# Função para limpar resultados antigos se necessário
cleanup_old_results() {
    local results_size=$(du -s diabetes/results 2>/dev/null | cut -f1)
    # Se o diretório de resultados for maior que 20GB (20971520 KB)
    if [ "$results_size" -gt 20971520 ]; then
        echo "Diretório de resultados muito grande ($(du -sh diabetes/results | cut -f1)). Limpando arquivos mais antigos..."
        # Remove arquivos de resultados com mais de 7 dias
        find diabetes/results -type f -mtime +7 -exec rm -f {} \; 2>/dev/null || true
        echo "Limpeza de resultados antigos concluída."
    fi
}

# Contadores
successful_trials=0
failed_trials=()

# Executa trials de 0 a 49
for trial in {0..49}; do
    echo "Executando trial $trial..."

    # Limpa resultados antigos se necessário (a cada 10 trials)
    if [ $((trial % 10)) -eq 0 ]; then
        cleanup_old_results
    fi

    # Verifica espaço em disco antes de cada trial
    if ! check_disk_space; then
        echo "Erro: Espaço em disco insuficiente para trial $trial"
        failed_trials+=($trial)
        continue
    fi

    if uv run python diabetes/run_model.py $trial; then
        echo "Trial $trial concluído com sucesso!"
        ((successful_trials++))
        # Limpa arquivos temporários após sucesso
        find /tmp -name ".tmp*" -type f -mmin +5 -exec rm -f {} \; 2>/dev/null || true
    else
        echo "Erro ao executar trial $trial"
        failed_trials+=($trial)
        # Limpa arquivos temporários após erro também
        find /tmp -name ".tmp*" -type f -mmin +5 -exec rm -f {} \; 2>/dev/null || true
    fi
done

# Relatório final
echo "=================================================="
echo "RELATÓRIO FINAL"
echo "=================================================="
echo "Trials executados com sucesso: $successful_trials/50"

if [ ${#failed_trials[@]} -gt 0 ]; then
    echo "Trials que falharam: ${failed_trials[*]}"
else
    echo "Todos os trials foram executados com sucesso!"
fi

# Para o monitor de disco se estiver rodando
if [ ! -z "$MONITOR_PID" ]; then
    echo "Parando monitor de disco (PID: $MONITOR_PID)..."
    kill $MONITOR_PID 2>/dev/null || true
fi

echo "=================================================="
