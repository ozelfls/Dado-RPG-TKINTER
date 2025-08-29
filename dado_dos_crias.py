import random
import tkinter as tk
import ttkbootstrap as tb
from tkinter import messagebox
from datetime import datetime

class DiceRollerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rolagem de Dados Avançada")
        self.root.geometry("520x760")

        # Tema inicial escuro
        self.style = tb.Style("darkly")
        self.is_dark = True

        self.current_result = tk.StringVar()
        self.current_result.set("Selecione um dado e clique em Rolar!")
        self.last_roll = None
        self.modifier = tk.IntVar(value=0)
        self.roll_mode = tk.StringVar(value="normal")
        self.num_dice = tk.IntVar(value=1)
        self.history = []

        # --- Botão alternar tema ---
        self.theme_button = tb.Button(
            root,
            text="🌙 Alternar Tema",
            bootstyle="secondary-outline",
            command=self.toggle_theme
        )
        self.theme_button.pack(pady=5)

        main_frame = tb.Frame(root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.result_label = tb.Label(
            main_frame,
            textvariable=self.current_result,
            wraplength=480,
            justify="center",
            font=("Helvetica", 14, "bold")
        )
        self.result_label.pack(pady=15)

        # --- Seção de escolha do dado ---
        dice_frame = tb.Labelframe(main_frame, text="Tipo de Dado", bootstyle="primary", padding=10)
        dice_frame.pack(fill=tk.X, pady=8)

        self.dice_type = tk.StringVar(value="d20")
        dice_options = [
            ("D4 (4 lados)", "d4"),
            ("D6 (6 lados)", "d6"),
            ("D8 (8 lados)", "d8"),
            ("D10 (10 lados)", "d10"),
            ("D12 (12 lados)", "d12"),
            ("D20 (20 lados)", "d20"),
            ("D100 (1-100)", "d100"),
            ("D% (10% a 100%)", "dpercent"),
        ]
        
        # Organizar os botões em duas colunas
        radio_frame = tb.Frame(dice_frame)
        radio_frame.pack(fill=tk.X)
        
        left_frame = tb.Frame(radio_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_frame = tb.Frame(radio_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Guardar referências para aplicar transição/estilo
        self.radio_buttons = []
        for i, (text, val) in enumerate(dice_options):
            frame = left_frame if i < 4 else right_frame
            rb = tb.Radiobutton(frame, text=text, variable=self.dice_type, value=val, bootstyle="info-round-toggle")
            rb.pack(anchor="w", pady=2)
            self.radio_buttons.append(rb)

        # --- Quantidade de dados ---
        quantity_frame = tb.Labelframe(main_frame, text="Quantidade de Dados", bootstyle="primary", padding=10)
        quantity_frame.pack(fill=tk.X, pady=8)

        tb.Label(quantity_frame, text="Número de dados (1-8):").pack(side="left")
        self.dice_quantity = tb.Spinbox(quantity_frame, from_=1, to=8, textvariable=self.num_dice, width=5, bootstyle="success")
        self.dice_quantity.pack(side="left", padx=8)

        # --- Modo de rolagem ---
        mode_frame = tb.Labelframe(main_frame, text="Modo de Rolagem", bootstyle="primary", padding=10)
        mode_frame.pack(fill=tk.X, pady=8)

        self.mode_buttons = []
        for text, val in [("Normal", "normal"), ("Vantagem", "vantagem"), ("Desvantagem", "desvantagem")]:
            rb = tb.Radiobutton(mode_frame, text=text, variable=self.roll_mode, value=val, bootstyle="info-round-toggle")
            rb.pack(anchor="w", pady=2)
            self.mode_buttons.append(rb)

        # --- Modificador ---
        modifier_frame = tb.Labelframe(main_frame, text="Modificador", bootstyle="primary", padding=10)
        modifier_frame.pack(fill=tk.X, pady=8)

        tb.Label(modifier_frame, text="Adicionar modificador:").pack(side="left")
        self.modifier_spinbox = tb.Spinbox(modifier_frame, from_=-10, to=10, textvariable=self.modifier, width=5, bootstyle="warning")
        self.modifier_spinbox.pack(side="left", padx=8)

        # --- Botões principais ---
        button_frame = tb.Frame(main_frame)
        button_frame.pack(pady=20)

        self.roll_button = tb.Button(button_frame, text="🎲 Rolar", bootstyle="success-outline", command=self.roll_dice, width=10)
        self.roll_button.pack(side="left", padx=8)

        self.reroll_button = tb.Button(button_frame, text="🔄 Rerolar (Desvantagem)", bootstyle="info-outline", command=self.reroll_dice, state="disabled", width=20)
        self.reroll_button.pack(side="left", padx=8)

        self.reset_button = tb.Button(button_frame, text="⏹ Resetar", bootstyle="danger-outline", command=self.reset_dice, width=10)
        self.reset_button.pack(side="left", padx=8)

        # --- Histórico ---
        secondary_button_frame = tb.Frame(main_frame)
        secondary_button_frame.pack(pady=10)

        self.history_button = tb.Button(secondary_button_frame, text="📜 Histórico", bootstyle="secondary-outline", command=self.show_history, width=15)
        self.history_button.pack(side="left", padx=8)

        self.clear_history_button = tb.Button(secondary_button_frame, text="🗑 Limpar Histórico", bootstyle="danger-outline", command=self.clear_history, width=15)
        self.clear_history_button.pack(side="left", padx=8)

    # -------- Alternância de tema --------
    def toggle_theme(self):
        """Alterna entre 'darkly' e 'flatly' e ajusta estilos dos widgets."""
        if self.is_dark:
            # Modo claro
            self.style.theme_use("flatly")
            self.is_dark = False

            # Toggles pretos
            for rb in self.radio_buttons + self.mode_buttons:
                self.smooth_transition(rb, "dark-round-toggle")

            # Botões principais sólidos
            self.roll_button.configure(bootstyle="success")
            self.reroll_button.configure(bootstyle="info")
            self.reset_button.configure(bootstyle="danger")
            self.history_button.configure(bootstyle="secondary")
            self.clear_history_button.configure(bootstyle="danger")

            # Botão de tema mais coerente no claro
            self.theme_button.configure(text="🌞 Alternar Tema", bootstyle="secondary")
        else:
            # Modo escuro
            self.style.theme_use("darkly")
            self.is_dark = True

            # Toggles azuis
            for rb in self.radio_buttons + self.mode_buttons:
                self.smooth_transition(rb, "info-round-toggle")

            # Botões principais outline
            self.roll_button.configure(bootstyle="success-outline")
            self.reroll_button.configure(bootstyle="info-outline")
            self.reset_button.configure(bootstyle="danger-outline")
            self.history_button.configure(bootstyle="secondary-outline")
            self.clear_history_button.configure(bootstyle="danger-outline")

            # Botão de tema no escuro
            self.theme_button.configure(text="🌙 Alternar Tema", bootstyle="secondary-outline")

    def smooth_transition(self, widget, new_style, steps=8, delay=18):
        """
        Simula uma transição suave: aplica um pequeno atraso antes de trocar o estilo.
        (ttkbootstrap não tiene animación nativa de colores en widgets)
        """
        def step(count=0):
            if count >= steps:
                widget.configure(bootstyle=new_style)
                return
            self.root.after(delay, lambda: step(count + 1))
        step()

    # -------- Funções de rolagem --------
    def roll_d4(self):
        return random.randint(1, 4)
    
    def roll_d6(self):
        return random.randint(1, 6)
    
    def roll_d8(self):
        return random.randint(1, 8)
    
    def roll_d10(self):
        return random.randint(1, 10)
    
    def roll_d12(self):
        return random.randint(1, 12)
    
    def roll_d20(self):
        return random.randint(1, 20)
    
    def roll_d100(self):
        return random.randint(1, 100)
    
    def roll_dpercent(self):
        return random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    
    def roll_dice(self):
        modifier = self.modifier.get()
        dice = self.dice_type.get()
        mode = self.roll_mode.get()
        quantity = self.num_dice.get()
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Determina qual função de rolagem usar
        roll_functions = {
            "d4": self.roll_d4,
            "d6": self.roll_d6,
            "d8": self.roll_d8,
            "d10": self.roll_d10,
            "d12": self.roll_d12,
            "d20": self.roll_d20,
            "d100": self.roll_d100,
            "dpercent": self.roll_dpercent
        }
        
        roll_func = roll_functions[dice]
        is_percent = (dice == "dpercent")
        is_d20 = (dice == "d20")
        
        all_rolls = []
        for _ in range(quantity):
            if mode == "normal":
                roll = roll_func()
                all_rolls.append(str(roll) + ("%" if is_percent else ""))
            else:
                roll1 = roll_func()
                roll2 = roll_func()
                roll = max(roll1, roll2) if mode == "vantagem" else min(roll1, roll2)
                roll_str = f"{roll1}{'%' if is_percent else ''}/{roll2}{'%' if is_percent else ''}→{roll}{'%' if is_percent else ''}"
                all_rolls.append(roll_str)
        
        # Verifica se há críticos (apenas para d20)
        critical_text = ""
        if is_d20 and quantity == 1:
            roll_value = int(all_rolls[0].split('→')[-1]) if '→' in all_rolls[0] else int(all_rolls[0])
            if roll_value == 20:
                critical_text = " - 🗿 SUCESSO CRÍTICO!"
                self.result_label.configure(foreground="#0080ff")  # Azul para sucesso crítico
            elif roll_value == 1:
                critical_text = " - 💀 FALHA CRÍTICA!"
                self.result_label.configure(foreground="#ff0000")  # Vermelho para falha crítica
            else:
                self.result_label.configure(foreground="white")  # Cor normal
        else:
            self.result_label.configure(foreground="white")  # Cor normal
        
        # Aplica modificador se necessário
        if modifier != 0:
            if dice == "d6" and quantity > 1:
                # Caso especial: d6 com múltiplos dados soma primeiro
                total = sum(int(r.split('→')[-1].replace('%', '')) if '→' in r else int(r.replace('%', '')) for r in all_rolls)
                final = total + modifier
                result_text = f"Resultado: {total} + {modifier} = {final} (d6 x{quantity}){critical_text}"
            else:
                modified_rolls = []
                for r in all_rolls:
                    roll_value = int(r.split('→')[-1].replace('%', '')) if '→' in r else int(r.replace('%', ''))
                    modified_value = roll_value + modifier
                    modified_rolls.append(f"{modified_value}{'%' if is_percent else ''}")
                
                mod_text = f" {'+' if modifier > 0 else ''}{modifier}{'%' if is_percent else ''} = "
                result_text = f"Resultados: {', '.join(all_rolls)}{mod_text}{', '.join(modified_rolls)}{critical_text}"
        else:
            if dice == "d6" and quantity > 1:
                total = sum(int(r.split('→')[-1]) if '→' in r else int(r) for r in all_rolls)
                result_text = f"Resultado: {total} (d6 x{quantity}){critical_text}"
            else:
                result_text = f"Resultados: {', '.join(all_rolls)}{critical_text}"
        
        # Salva no histórico
        history_entry = {
            'timestamp': timestamp,
            'type': f"{dice} x{quantity}",
            'mode': mode,
            'modifier': modifier,
            'rolls': all_rolls,
            'display': result_text
        }
        
        self.history.append(history_entry)
        self.last_roll = (dice, quantity, modifier, mode)
        self.current_result.set(result_text)
        self.reroll_button.config(state="normal")
    
    def reroll_dice(self):
        if self.last_roll:
            dice, quantity, modifier, original_mode = self.last_roll
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Força o modo desvantagem para rerol
            mode = "desvantagem"
            
            # Determina qual função de rolagem usar
            roll_functions = {
                "d4": self.roll_d4,
                "d6": self.roll_d6,
                "d8": self.roll_d8,
                "d10": self.roll_d10,
                "d12": self.roll_d12,
                "d20": self.roll_d20,
                "d100": self.roll_d100,
                "dpercent": self.roll_dpercent
            }
            
            roll_func = roll_functions[dice]
            is_percent = (dice == "dpercent")
            is_d20 = (dice == "d20")
            
            all_rolls = []
            for _ in range(quantity):
                # Sempre rola em desvantagem (rola 2 e pega o menor)
                roll1 = roll_func()
                roll2 = roll_func()
                roll = min(roll1, roll2)
                roll_str = f"{roll1}{'%' if is_percent else ''}/{roll2}{'%' if is_percent else ''}→{roll}{'%' if is_percent else ''}"
                all_rolls.append(roll_str)
            
            # Verifica se há críticos (apenas para d20)
            critical_text = ""
            if is_d20 and quantity == 1:
                roll_value = int(all_rolls[0].split('→')[-1]) if '→' in all_rolls[0] else int(all_rolls[0])
                if roll_value == 20:
                    critical_text = " - 🗿 SUCESSO CRÍTICO!"
                    self.result_label.configure(foreground="#0080ff")
                elif roll_value == 1:
                    critical_text = " - 💀 FALHA CRÍTICA!"
                    self.result_label.configure(foreground="#ff0000")
                else:
                    self.result_label.configure(foreground="white")
            else:
                self.result_label.configure(foreground="white")
            
            # Aplica modificador se necessário
            if modifier != 0:
                if dice == "d6" and quantity > 1:
                    total = sum(int(r.split('→')[-1].replace('%', '')) if '→' in r else int(r.replace('%', '')) for r in all_rolls)
                    final = total + modifier
                    result_text = f"Rerol (Desvantagem): {total} + {modifier} = {final} (d6 x{quantity}){critical_text}"
                else:
                    modified_rolls = []
                    for r in all_rolls:
                        roll_value = int(r.split('→')[-1].replace('%', '')) if '→' in r else int(r.replace('%', ''))
                        modified_value = roll_value + modifier
                        modified_rolls.append(f"{modified_value}{'%' if is_percent else ''}")
                    
                    mod_text = f" {'+' if modifier > 0 else ''}{modifier}{'%' if is_percent else ''} = "
                    result_text = f"Rerol (Desvantagem): {', '.join(all_rolls)}{mod_text}{', '.join(modified_rolls)}{critical_text}"
            else:
                if dice == "d6" and quantity > 1:
                    total = sum(int(r.split('→')[-1]) if '→' in r else int(r) for r in all_rolls)
                    result_text = f"Rerol (Desvantagem): {total} (d6 x{quantity}){critical_text}"
                else:
                    result_text = f"Rerol (Desvantagem): {', '.join(all_rolls)}{critical_text}"
            
            # Salva no histórico
            history_entry = {
                'timestamp': timestamp,
                'type': f"{dice} x{quantity}",
                'mode': mode,
                'modifier': modifier,
                'rolls': all_rolls,
                'display': result_text
            }
            
            self.history.append(history_entry)
            self.current_result.set(result_text)
    
    def reset_dice(self):
        self.current_result.set("Selecione um dado e clique em Rolar!")
        self.last_roll = None
        self.reroll_button.config(state="disabled")
        self.result_label.configure(foreground="white")
    
    def show_history(self):
        if not self.history:
            messagebox.showinfo("Histórico", "Nenhum lançamento registrado ainda!")
            return
            
        history_window = tb.Toplevel(self.root)
        history_window.title("Histórico de Lançamentos")
        history_window.geometry("700x400")
        
        main_frame = tb.Frame(history_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tb.Scrollbar(main_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Aplicando a cor verde do botão rolar (#35E22C) ao fundo do histórico
        history_listbox = tk.Listbox(
            main_frame,
            yscrollcommand=scrollbar.set,
            font=('Courier', 10),
            selectmode=tk.SINGLE,
            width=90,
            height=20,
            bg="#35E22C",  # Verde do botão rolar
            fg="white",
            selectbackground="#2AB825",  # Verde mais escuro para seleção
            selectforeground="white"
        )
        history_listbox.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=history_listbox.yview)
        
        for idx, entry in enumerate(reversed(self.history)):
            display_text = f"[{entry['timestamp']}] {entry['display']}"
            history_listbox.insert(tk.END, display_text)
        
        close_button = tb.Button(
            history_window,
            text="Fechar",
            command=history_window.destroy,
            bootstyle="secondary-outline"
        )
        close_button.pack(pady=10)
    
    def clear_history(self):
        self.history = []
        messagebox.showinfo("Histórico", "Histórico de lançamentos limpo com sucesso!")

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = DiceRollerApp(root)
    root.mainloop()