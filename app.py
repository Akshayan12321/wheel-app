import tkinter as tk
import random
import math

COLORS = [
    ("Red", "#E53935", "Most Billed Hours", ""),
    ("Orange", "#FB8C00", "Least Missed SLA", ""),
    ("Yellow", "#FDD835", "Kill Rate", ""),
    ("Green", "#43A047", "CSAT Leader", ""),
    ("Blue", "#1E88E5", "Resolved Tickets", ""),
    ("Purple", "#8E24AA", "Avg. Ticket Resolve", ""),
    ("Pink", "#EC407A", "Avg. Response Time", "")
]

angle = 0
spinning = False
recent_winners = []
winner_history = []
config_window = None

def update_history(metric_name, person_name):
    if person_name:
        full_text = f"{metric_name}  ➔  {person_name}"
    else:
        full_text = metric_name
        
    winner_history.append(full_text)
    history_listbox.insert(
        tk.END,
        f"  {len(winner_history)}.  {full_text}"
    )
    history_listbox.yview_moveto(1.0)
    if history_listbox.size() > 50:
        history_listbox.delete(0)

def draw_wheel(event=None):
    canvas.delete("all")
    
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    
    if width < 10 or height < 10:
        return
        
    center_x = width / 2
    center_y = height / 2
    
    radius = min(center_x, center_y) - 45
    if radius < 80:
        radius = 80

    # Outer deep shadow
    canvas.create_oval(
        center_x - radius - 16,
        center_y - radius - 16,
        center_x + radius + 16,
        center_y + radius + 16,
        fill="#150e00",
        outline=""
    )
    # Gold rim shadow
    canvas.create_oval(
        center_x - radius - 8,
        center_y - radius - 8,
        center_x + radius + 8,
        center_y + radius + 8,
        fill="#614700",
        outline=""
    )
    # Main gold rim
    rim_width = max(3, int(radius * 0.02))
    canvas.create_oval(
        center_x - radius,
        center_y - radius,
        center_x + radius,
        center_y + radius,
        fill="#d4af37",
        outline="#fff6c7",
        width=rim_width
    )
    
    section = 360 / len(COLORS)
    for i, (name, colour, metric_name, person_name) in enumerate(COLORS):
        start = angle + i * section
        canvas.create_arc(
            center_x - radius + 12,
            center_y - radius + 12,
            center_x + radius - 12,
            center_y + radius - 12,
            start=start,
            extent=section,
            fill=colour,
            outline="#1a1a1a",
            width=2
        )
        mid = start + section / 2
        
        text_dist = radius * 0.65
        x = center_x + text_dist * math.cos(math.radians(mid))
        y = center_y - text_dist * math.sin(math.radians(mid))
        
        font_size = max(9, int(radius * 0.045))
        
        if person_name:
            display_text = f"{metric_name}\n({person_name})"
        else:
            display_text = metric_name
        
        # Multi-directional shadow/outline for extreme readability against any color background
        for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, 1.5), (1.5, 0)]:
            canvas.create_text(
                x + dx,
                y + dy,
                text=display_text,
                fill="#000000",
                font=("Segoe UI", font_size, "bold"),
                justify="center"
            )
            
        # Crisp pure white primary text
        canvas.create_text(
            x,
            y,
            text=display_text,
            fill="#ffffff",
            font=("Segoe UI", font_size, "bold"),
            justify="center"
        )
        
    btn_outer = radius * 0.38
    btn_inner = radius * 0.32
    
    # Center Spin Button (Shadow/oval layers removed completely for a clean look)
    canvas.create_oval(
        center_x - btn_outer,
        center_y - btn_outer,
        center_x + btn_outer,
        center_y + btn_outer,
        fill="#d4af37",
        outline="#fff9db",
        width=3,
        tags="spin"
    )
    canvas.create_oval(
        center_x - btn_inner,
        center_y - btn_inner,
        center_x + btn_inner,
        center_y + btn_inner,
        fill="#b30000",
        outline="#ffcc66",
        width=2,
        tags="spin"
   
    )
    
    spin_font_size = max(11, int(radius * 0.09))
    canvas.create_text(
        center_x,
        center_y,
        text="SPIN",
        fill="#fff9db",
        font=("Segoe UI", spin_font_size, "bold"),
        tags="spin"
    )
    
    ptr_half_width = max(10, int(radius * 0.1))
    ptr_tip_y = center_y - radius - 5
    ptr_base_y = ptr_tip_y - max(20, int(radius * 0.25))
    
    canvas.create_polygon(
        center_x,
        ptr_tip_y,
        center_x - ptr_half_width,
        ptr_base_y,
        center_x + ptr_half_width,
        ptr_base_y,
        fill="#d4af37",
        outline="#fff9db",
        width=2
    )
    
    canvas.tag_bind(
        "spin",
        "<Button-1>",
        lambda e: spin()
    )

def finish_spin():
    global spinning
    spinning = False
    section = 360 / len(COLORS)
    pointer_angle = (90 - angle) % 360
    winner = int(pointer_angle / section)
    winner %= len(COLORS)
    
    recent_winners.append(winner)
    if len(recent_winners) > 2:
        recent_winners.pop(0)

    colour_name = COLORS[winner][0]
    colour_hex = COLORS[winner][1]
    metric_name = COLORS[winner][2]
    person_name = COLORS[winner][3]
    
    if person_name:
        result_str = f"{metric_name} ({person_name})"
    else:
        result_str = metric_name

    result_label.config(
        text=f"WINNER: {result_str}",
        fg=colour_hex
    )
    update_history(metric_name, person_name)

def animate(speed):
    global angle
    if speed > 1:
        angle += speed
        draw_wheel()
        speed *= 0.965
        window.after(
            16,
            lambda: animate(speed)
        )
    else:
        finish_spin()

def spin():
    global spinning
    global recent_winners
    if spinning:
        return
    spinning = True
    result_label.config(
        text="Spinning...",
        fg="#d4af37"
    )
    
    while True:
        test_angle = angle
        test_speed = random.randint(35, 45)
        
        sim_speed = test_speed
        sim_angle = test_angle
        while sim_speed > 1:
            sim_angle += sim_speed
            sim_speed *= 0.965
            
        section = 360 / len(COLORS)
        pointer_angle = (90 - sim_angle) % 360
        winner = int(pointer_angle / section)
        winner %= len(COLORS)
        
        if winner not in recent_winners:
            animate(test_speed)
            break

def reset_all():
    global angle, spinning, recent_winners, winner_history
    if spinning:
        return
    
    angle = 0
    recent_winners.clear()
    winner_history.clear()
    history_listbox.delete(0, tk.END)
    result_label.config(
        text="Click SPIN on the Wheel",
        fg="#d4af37"
    )
    draw_wheel()

def open_config_window():
    global config_window
    if spinning:
        return
        
    if config_window is not None and config_window.winfo_exists():
        config_window.lift()
        return

    config_window = tk.Toplevel(window)
    config_window.title("Configure Names")
    config_window.geometry("480x560")
    config_window.configure(bg="#111111")
    config_window.resizable(False, False)

    tk.Label(
        config_window,
        text="Assign Names to Metrics",
        bg="#111111",
        fg="#d4af37",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=15)

    entries = []
    
    form_frame = tk.Frame(config_window, bg="#111111")
    form_frame.pack(pady=5, padx=25, fill="x")

    for i, (color_name, colour_hex, metric_name, current_person) in enumerate(COLORS):
        row_frame = tk.Frame(form_frame, bg="#1a1a1a", highlightbackground="#d4af37", highlightthickness=1)
        row_frame.pack(fill="x", pady=6)
        
        tk.Label(
            row_frame,
            text=metric_name,
            bg="#1a1a1a",
            fg="#fff9db",
            font=("Segoe UI", 11, "bold"),
            width=20,
            anchor="w"
        ).pack(side="left", padx=10, pady=8)
        
        entry = tk.Entry(
            row_frame,
            bg="#050505",
            fg="#d4af37",
            insertbackground="#d4af37",
            font=("Segoe UI", 12, "bold"),
            relief="flat"
        )
        entry.insert(0, str(current_person))
        entry.pack(side="right", expand=True, fill="both", padx=10, pady=8)
        entries.append((i, entry))

    def save_names():
        for i, entry in entries:
            new_person = entry.get().strip()
            COLORS[i] = (COLORS[i][0], COLORS[i][1], COLORS[i][2], new_person)
        draw_wheel()
        config_window.destroy()

    save_btn = tk.Button(
        config_window,
        text="SAVE NAMES",
        bg="#d4af37",
        fg="#111111",
        activebackground="#ffe8a3",
        activeforeground="#111111",
        font=("Segoe UI", 13, "bold"),
        relief="flat",
        cursor="hand2",
        command=save_names
    )
    save_btn.pack(pady=25, padx=25, fill="x", ipady=8)

# Main Application Window
window = tk.Tk()
window.title("Spin Wheel")
window.geometry("1200x750")
window.configure(bg="#0b0b0b")
window.minsize(900, 600)

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=3)
window.columnconfigure(1, weight=2)

# ==================== LEFT COLUMN (Wheel Area) ====================
left_frame = tk.Frame(window, bg="#0b0b0b")
left_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
left_frame.rowconfigure(1, weight=1)
left_frame.columnconfigure(0, weight=1)

title = tk.Label(
    left_frame,
    text="",
    bg="#0b0b0b",
    fg="#d4af37",
    font=("Segoe UI", 18, "bold")
)
title.grid(row=0, column=0, pady=(0, 5))

canvas = tk.Canvas(
    left_frame,
    bg="#0b0b0b",
    highlightthickness=0
)
canvas.grid(row=1, column=0, sticky="nsew")

canvas.bind("<Configure>", draw_wheel)

# ==================== RIGHT COLUMN (History & Controls) ====================
right_frame = tk.Frame(window, bg="#0b0b0b")
right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
right_frame.rowconfigure(3, weight=1)
right_frame.columnconfigure(0, weight=1)

winner_frame = tk.Frame(
    right_frame,
    bg="#141414",
    highlightbackground="#d4af37",
    highlightthickness=2
)
winner_frame.grid(row=0, column=0, sticky="ew", pady=(5, 10))

result_label = tk.Label(
    winner_frame,
    text="Click SPIN on the Wheel",
    bg="#141414",
    fg="#d4af37",
    font=("Segoe UI", 16, "bold")
)
result_label.pack(pady=12, padx=10)

button_frame = tk.Frame(right_frame, bg="#0b0b0b")
button_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

config_button = tk.Button(
    button_frame,
    text="⚙️ CONFIGURE NAMES",
    bg="#1c1c1c",
    fg="#d4af37",
    activebackground="#2b2b2b",
    activeforeground="#ffe8a3",
    font=("Segoe UI", 10, "bold"),
    relief="solid",
    bd=1,
    highlightbackground="#d4af37",
    cursor="hand2",
    command=open_config_window
)
config_button.grid(row=0, column=0, sticky="ew", padx=(0, 5), ipady=6)

reset_button = tk.Button(
    button_frame,
    text="🔄 RESET WHEEL",
    bg="#1c1c1c",
    fg="#d4af37",
    activebackground="#2b2b2b",
    activeforeground="#ffe8a3",
    font=("Segoe UI", 10, "bold"),
    relief="solid",
    bd=1,
    highlightbackground="#d4af37",
    cursor="hand2",
    command=reset_all
)
reset_button.grid(row=0, column=1, sticky="ew", padx=(5, 0), ipady=6)

history_title = tk.Label(
    right_frame,
    text="📜 Winner History",
    bg="#0b0b0b",
    fg="#d4af37",
    font=("Segoe UI", 14, "bold")
)
history_title.grid(row=2, column=0, sticky="w", pady=(0, 5))

history_frame = tk.Frame(
    right_frame,
    bg="#141414",
    highlightbackground="#d4af37",
    highlightthickness=2
)
history_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 5))

history_listbox = tk.Listbox(
    history_frame,
    bg="#141414",
    fg="#ffe8a3",
    font=("Segoe UI", 11, "bold"),
    borderwidth=0,
    highlightthickness=0
)
history_listbox.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

window.mainloop()
