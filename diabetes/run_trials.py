#!/usr/bin/env python3
"""
Script para executar o modelo de diabetes com diferentes valores de trial.
Executa o run_model.py com valores de trial de 0 a 49.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_trial(trial_number):
    """
    Executa o run_model.py com um valor específico de trial.
    
    Args:
        trial_number (int): Número do trial a ser executado
    """
    print(f"Executando trial {trial_number}...")
    
    try:
        # Executa o script run_model.py com o parâmetro trial
        result = subprocess.run([
            sys.executable, 
            "diabetes/run_model.py", 
            str(trial_number)
        ], 
        check=True, 
        capture_output=True, 
        text=True
        )
        
        print(f"Trial {trial_number} concluído com sucesso!")
        if result.stdout:
            print(f"Output: {result.stdout}")
            
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar trial {trial_number}: {e}")
        if e.stderr:
            print(f"Erro: {e.stderr}")
        return False
    
    return True

def main():
    """
    Função principal que executa todos os trials de 0 a 49.
    """
    print("Iniciando execução dos trials...")
    
    # Verifica se o arquivo run_model.py existe
    if not os.path.exists("diabetes/run_model.py"):
        print("Erro: Arquivo diabetes/run_model.py não encontrado!")
        sys.exit(1)
    
    # Executa trials de 0 a 49
    successful_trials = 0
    failed_trials = []
    
    for trial in range(50):
        success = run_trial(trial)
        if success:
            successful_trials += 1
        else:
            failed_trials.append(trial)
    
    # Relatório final
    print("\n" + "="*50)
    print("RELATÓRIO FINAL")
    print("="*50)
    print(f"Trials executados com sucesso: {successful_trials}/50")
    
    if failed_trials:
        print(f"Trials que falharam: {failed_trials}")
    else:
        print("Todos os trials foram executados com sucesso!")
    
    print("="*50)

if __name__ == "__main__":
    main()
