import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import csv
import os

# 16 QUESTIONS - Academic Portfolio Building and Progress Visualization
questions = [
    ("How often do you update your academic portfolio?", ["Never","Rarely","Sometimes","Often","Always"], [0,1,2,3,4]),
    ("How effective is your current portfolio for visualizing progress?", ["Not effective","Slightly effective","Moderately effective","Very effective","Extremely effective"], [0,1,2,3,4]),
    ("Do you set clear academic goals in your portfolio?", ["Never","Rarely","Sometimes","Often","Always"], [0,1,2,3,4]),
    ("How confident are you in tracking your academic progress?", ["Not confident","Slightly confident","Moderately confident","Very confident","Extremely confident"], [0,1,2,3,4]),
    ("How often do you review your past academic achievements?", ["Never","Rarely","Sometimes","Often","Always"], [0,1,2,3,4]),
    ("Does your portfolio help you identify your strengths and weaknesses?", ["Not at all","Slightly","Moderately","Very much","Completely"], [0,1,2,3,4]),
    ("How organized is your academic portfolio?", ["Very disorganized","Disorganized","Neutral","Organized","Very organized"], [0,1,2,3,4]),
    ("How often do you use visual tools (charts, graphs) in your portfolio?", ["Never","Rarely","Sometimes","Often","Always"], [0,1,2,3,4]),
    ("Does portfolio building motivate you to improve academically?", ["Not at all","Slightly","Moderately","Very much","Completely"], [0,1,2,3,4]),
    ("How easy is it for you to find past work in your portfolio?", ["Very difficult","Difficult","Neutral","Easy","Very easy"], [0,1,2,3,4]),
    ("How often do you share your portfolio with mentors or peers?", ["Never","Rarely","Sometimes","Often","Always"], [0,1,2,3,4]),
    ("Does your portfolio reflect your academic growth over time?", ["Not at all","Slightly","Moderately","Very much","Completely"], [0,1,2,3,4]),
    ("How satisfied are you with your current portfolio system?", ["Very unsatisfied","Unsatisfied","Neutral","Satisfied","Very satisfied"], [0,1,2,3,4]),
    ("How often do you add new evidence of learning to your portfolio?", ["Never","Rarely","Sometimes","Often","Always"], [0,1,2,3,4]),
    ("Does portfolio building help you plan your future academic steps?", ["Not at all","Slightly","Moderately","Very much","Completely"], [0,1,2,3,4]),
    ("Overall, how effective is your portfolio for visualizing academic progress?", ["Not effective","Slightly effective","Moderately effective","Very effective","Extremely effective"], [0,1,2,3,4])
]

def get_effectiveness_level(score):
    """Return effectiveness level and portfolio status based on score"""
    if score <= 12:
        return "Very Low Effectiveness - Portfolio needs major improvement.", "Needs Urgent Revision"
    elif score <= 24:
        return "Low Effectiveness - Portfolio requires significant work.", "Below Average"
    elif score <= 36:
        return "Moderate Effectiveness - Portfolio is acceptable but can improve.", "Satisfactory"
    elif score <= 48:
        return "Good Effectiveness - Portfolio works well for progress visualization.", "Good"
    elif score <= 60:
        return "High Effectiveness - Portfolio is very effective.", "Very Good"
    else:
        return "Excellent Effectiveness - Portfolio is highly effective for tracking progress.", "Excellent"

def valid_name(s):
    return s and all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ- ' " for c in s)

def valid_dob(dob_str):
    try:
        dob = datetime.strptime(dob_str, "%d-%m-%y")
        return dob <= datetime.now()
    except:
        return False

class PortfolioSurveyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Academic Portfolio Effectiveness Survey")
        self.root.geometry("650x550")
        
        self.answers = []
        self.current_q = 0
        self.score = 0
        self.user_data = {}
        
        self.show_info_page()
    
    def show_info_page(self):
        self.clear_frame()
        
        tk.Label(self.root, text="ACADEMIC PORTFOLIO SURVEY", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.root, text="Personal Information", font=("Arial", 12)).pack(pady=5)
        
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        
        tk.Label(frame, text="Surname:").grid(row=0, column=0, sticky="e", pady=5)
        self.surname_entry = tk.Entry(frame, width=30)
        self.surname_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(frame, text="Given name:").grid(row=1, column=0, sticky="e", pady=5)
        self.given_entry = tk.Entry(frame, width=30)
        self.given_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="Date of Birth (DD-MM-YY):").grid(row=2, column=0, sticky="e", pady=5)
        self.dob_entry = tk.Entry(frame, width=30)
        self.dob_entry.grid(row=2, column=1, pady=5)
        self.dob_entry.insert(0, "01-01-01")
        
        tk.Label(frame, text="Student ID (5 digits):").grid(row=3, column=0, sticky="e", pady=5)
        self.sid_entry = tk.Entry(frame, width=30)
        self.sid_entry.grid(row=3, column=1, pady=5)
        self.sid_entry.insert(0, "12345")
        
        tk.Button(self.root, text="Start Survey", command=self.validate_and_start, bg="green", fg="white", padx=20, pady=5).pack(pady=20)
    
    def validate_and_start(self):
        surname = self.surname_entry.get().strip()
        given = self.given_entry.get().strip()
        dob = self.dob_entry.get().strip()
        sid_input = self.sid_entry.get().strip()
        
        if not valid_name(surname):
            messagebox.showerror("Error", "Invalid surname! Use letters, -, ', spaces only.")
            return
        if not valid_name(given):
            messagebox.showerror("Error", "Invalid given name!")
            return
        if not valid_dob(dob):
            messagebox.showerror("Error", "Invalid DOB! Use DD-MM-YY (e.g., 01-01-01)")
            return
        if not (sid_input.isdigit() and len(sid_input) == 5):
            messagebox.showerror("Error", "Student ID must be 5 digits (e.g., 12345)")
            return
        
        self.user_data = {
            "surname": surname,
            "given": given,
            "dob": dob,
            "sid": "000" + sid_input
        }
        
        self.score = 0
        self.current_q = 0
        self.show_question()
    
    def show_question(self):
        self.clear_frame()
        
        if self.current_q >= len(questions):
            self.show_results()
            return
        
        q_text, options, _ = questions[self.current_q]
        
        tk.Label(self.root, text=f"Question {self.current_q + 1} of {len(questions)}", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(self.root, text=q_text, font=("Arial", 11), wraplength=550).pack(pady=10)
        
        self.answer_var = tk.IntVar()
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        
        for i, opt in enumerate(options, 1):
            tk.Radiobutton(frame, text=f"{i}. {opt}", variable=self.answer_var, value=i, font=("Arial", 10)).pack(anchor="w", pady=2)
        
        tk.Button(self.root, text="Next", command=self.next_question, bg="blue", fg="white", padx=20, pady=5).pack(pady=20)
    
    def next_question(self):
        if not self.answer_var.get():
            messagebox.showwarning("Warning", "Please select an option")
            return
        
        _, _, scores = questions[self.current_q]
        self.score += scores[self.answer_var.get() - 1]
        self.current_q += 1
        self.show_question()
    
    def show_results(self):
        self.clear_frame()
        
        result, status = get_effectiveness_level(self.score)
        
        tk.Label(self.root, text="SURVEY RESULTS", font=("Arial", 14, "bold")).pack(pady=10)
        
        results_text = f"""
Name: {self.user_data['given']} {self.user_data['surname']}
Date of Birth: {self.user_data['dob']}
Student ID: {self.user_data['sid']}

Total Score: {self.score}/64
Portfolio Status: {status}

Assessment: {result}
"""
        tk.Label(self.root, text=results_text, font=("Arial", 10), justify="left").pack(pady=10)
        
        # Recommendation based on score
        if self.score <= 12:
            rec = "Consider rebuilding your portfolio structure. Add regular updates and visual progress tracking."
        elif self.score <= 24:
            rec = "Try to update your portfolio more frequently and use charts to visualize progress."
        elif self.score <= 36:
            rec = "Your portfolio is acceptable. Add more visual elements and set clearer academic goals."
        elif self.score <= 48:
            rec = "Good work! Keep maintaining your portfolio regularly."
        else:
            rec = "Excellent portfolio practices! Share your methods with other students."
        
        tk.Label(self.root, text=f"Recommendation: {rec}", font=("Arial", 10, "italic"), wraplength=550).pack(pady=10)
        
        tk.Button(self.root, text="Save Results", command=self.save_dialog, bg="green", fg="white", padx=20, pady=5).pack(pady=5)
        tk.Button(self.root, text="Back to Menu", command=self.show_menu, bg="gray", fg="white", padx=20, pady=5).pack(pady=5)
    
    def save_dialog(self):
        filetype = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv"), ("Text files", "*.txt")],
            title="Save Results"
        )
        if not filetype:
            return
        
        result, status = get_effectiveness_level(self.score)
        
        data = {
            "name": f"{self.user_data['given']} {self.user_data['surname']}",
            "dob": self.user_data['dob'],
            "student_id": self.user_data['sid'],
            "total_score": self.score,
            "portfolio_status": status,
            "assessment": result,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        ext = os.path.splitext(filetype)[1].lower()
        try:
            if ext == ".txt":
                with open(filetype, 'w', encoding='utf-8') as f:
                    f.write("ACADEMIC PORTFOLIO EFFECTIVENESS SURVEY\n")
                    f.write("="*50 + "\n")
                    for k, v in data.items():
                        f.write(f"{k}: {v}\n")
            elif ext == ".csv":
                with open(filetype, 'w', newline='', encoding='utf-8') as f:
                    w = csv.writer(f)
                    w.writerow(data.keys())
                    w.writerow(data.values())
            elif ext == ".json":
                with open(filetype, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
            else:
                messagebox.showerror("Error", "Unsupported format")
                return
            
            messagebox.showinfo("Success", f"Results saved to {filetype}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")
    
    def show_menu(self):
        self.clear_frame()
        
        tk.Label(self.root, text="MAIN MENU", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Button(self.root, text="Start New Survey", command=self.show_info_page, bg="green", fg="white", padx=20, pady=10, width=25).pack(pady=10)
        tk.Button(self.root, text="Load Saved Results", command=self.load_results_dialog, bg="blue", fg="white", padx=20, pady=10, width=25).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, bg="red", fg="white", padx=20, pady=10, width=25).pack(pady=10)
    
    def load_results_dialog(self):
        filename = filedialog.askopenfilename(
            title="Load Results",
            filetypes=[("All supported", "*.txt *.csv *.json"), ("Text files", "*.txt"), ("CSV files", "*.csv"), ("JSON files", "*.json")]
        )
        if not filename:
            return
        
        self.clear_frame()
        tk.Label(self.root, text="LOADED RESULTS", font=("Arial", 14, "bold")).pack(pady=10)
        
        try:
            ext = os.path.splitext(filename)[1].lower()
            content = ""
            
            if ext == ".txt":
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif ext == ".csv":
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        content += " | ".join(row) + "\n"
            elif ext == ".json":
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for k, v in data.items():
                        content += f"{k}: {v}\n"
            else:
                messagebox.showerror("Error", "Unsupported format")
                self.show_menu()
                return
            
            text_widget = tk.Text(self.root, wrap="word", height=20, width=70)
            text_widget.pack(pady=10, padx=10)
            text_widget.insert("1.0", content)
            text_widget.config(state="disabled")
            
            tk.Button(self.root, text="Back to Menu", command=self.show_menu, bg="gray", fg="white", padx=20, pady=5).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {e}")
            self.show_menu()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioSurveyApp(root)
    root.mainloop()