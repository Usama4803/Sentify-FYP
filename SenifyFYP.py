import tkinter as tk
from tkinter import messagebox, filedialog
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import customtkinter
import pyrebase

class LoginSignupApp(tk.Tk):
    def __init__(self, auth):
        super().__init__()
        self.auth = auth
        self.title("Login Form")
        self.geometry("400x240")
        self.configure(bg="black")
        self.iconbitmap(r"C:\\Users\AQII\\Final Project\FYP\Login\favicon.ico")

        self.username_label = customtkinter.CTkLabel(
            master=self,
            text="Username",
            width=80,
            height=25,
            text_color="white",
            fg_color=("black", "white"),
            corner_radius=8
        )
        self.username_label.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        self.password_label = customtkinter.CTkLabel(
            master=self,
            text="Password",
            width=80,
            height=25,
            text_color="white",
            fg_color=("black", "white"),
            corner_radius=8
        )
        self.password_label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)

        self.login_username_entry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Username",
            width=180,
            height=25,
            border_width=2,
            corner_radius=10
        )
        self.login_username_entry.place(relx=0.65, rely=0.3, anchor=tk.CENTER)

        self.login_password_entry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Password",
            width=180,
            height=25,
            border_width=2,
            corner_radius=10
        )
        self.login_password_entry.place(relx=0.65, rely=0.5, anchor=tk.CENTER)

        self.login_button = customtkinter.CTkButton(
            master=self,
            width=80,
            height=32,
            border_width=0,
            corner_radius=8,
            text="Login",
            command=self.logon_task
        )
        self.login_button.place(relx=0.71, rely=0.7, anchor=tk.CENTER)

        self.signup_button = customtkinter.CTkButton(
            master=self,
            width=80,
            height=32,
            border_width=0,
            corner_radius=8,
            text="Sign Up",
            command=self.open_signup_window
        )
        self.signup_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.login_result_label = customtkinter.CTkLabel(
            master=self,
            text="",
            width=120,
            height=26,
            text_color="black",
            fg_color=("white", "white"),
            corner_radius=8
        )
        self.login_result_label.place(relx=0.62, rely=0.85, anchor=tk.CENTER)

    def logon_task(self):
        email = self.login_username_entry.get()
        password = self.login_password_entry.get()
        try:
            login = self.auth.sign_in_with_email_and_password(email, password)
            self.login_result_label.configure(text="Successfully logged in!")
            self.start_sentiment_analysis_app()  # Call the function to start the sentiment analysis app
        except Exception as e:
            self.login_result_label.configure(text="Invalid email or password")
            
    def start_sentiment_analysis_app(self):
        # Close the current login/signup window
        self.destroy()

        # Start the sentiment analysis application
        root = tk.Tk()
        app = SentimentAnalysisApp(root)
        root.iconbitmap(r"C:\\Users\AQII\\Final Project\FYP\Login\favicon.ico") 
        root.mainloop()

    def signup_task(self):
        email = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        try:
            login = auth.create_user_with_email_and_password(email, password)
            self.signup_result_label.configure(text="Successfully signed up!")
        except Exception as e:
            self.signup_result_label.configure(text="Email already exists")

    def open_signup_window(self):
        signup_window = SignupWindow(self, self.auth)

class SignupWindow(tk.Toplevel):
    def __init__(self, master, auth):
        super().__init__(master)
        self.auth = auth
        self.title("Sign Up")
        self.geometry("400x240")
        self.configure(bg="black")

        self.master = master

        self.username_label = customtkinter.CTkLabel(
            master=self,
            text="Username",
            width=80,
            height=25,
            text_color="white",
            fg_color=("black", "white"),
            corner_radius=8
        )
        self.username_label.place(relx=0.3, rely=0.3, anchor=tk.CENTER)

        self.password_label = customtkinter.CTkLabel(
            master=self,
            text="Password",
            width=80,
            height=25,
            text_color="white",
            fg_color=("black", "white"),
            corner_radius=8
        )
        self.password_label.place(relx=0.3, rely=0.5, anchor=tk.CENTER)

        self.signup_username_entry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Username",
            width=180,
            height=25,
            border_width=2,
            corner_radius=10
        )
        self.signup_username_entry.place(relx=0.65, rely=0.3, anchor=tk.CENTER)

        self.signup_password_entry = customtkinter.CTkEntry(
            master=self,
            placeholder_text="Password",
            width=180,
            height=25,
            border_width=2,
            corner_radius=10
        )
        self.signup_password_entry.place(relx=0.65, rely=0.5, anchor=tk.CENTER)

        self.signup_button = customtkinter.CTkButton(
            master=self,
            width=80,
            height=32,
            border_width=0,
            corner_radius=8,
            text="Sign Up",
            command=self.master.signup_task
        )
        self.signup_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.signup_result_label = customtkinter.CTkLabel(
            master=self,
            text="",
            width=120,
            height=26,
            text_color="black",
            fg_color=("white", "white"),
            corner_radius=8
        )
        self.signup_result_label.place(relx=0.62, rely=0.85, anchor=tk.CENTER)
        
class SentimentAnalysisApp:
    def __init__(self, master):
        self.master = master
        master.title("Sentify")
        # Color Scheme
        self.bg_color = "#f0f0f0"
        self.button_bg_color = "#4CAF50"
        self.button_fg_color = "#FFFFFF"
        self.text_color = "#333333"

        # Create menu
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)

        # Create file menu
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Load Text File", command=self.load_text_file)
        self.file_menu.add_command(label="Show Analysis History", command=self.show_analysis_history)
        self.file_menu.add_command(label="Word Count", command=self.update_word_count)
        self.file_menu.add_command(label="Exit", command=master.quit)

        # Create help menu
        self.help_menu = tk.Menu(self.menu, tearoff=False)
        self.about_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.menu.add_cascade(label="about",menu=self.about_menu)

        # Frame for review entry
        review_frame = tk.Frame(master, bd=2, relief=tk.GROOVE, bg=self.bg_color)
        review_frame.pack(pady=10)

        # Label and text for entering review
        self.label = tk.Label(review_frame, text="Enter your review:", bg=self.bg_color, fg=self.text_color)
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.review_entry = tk.Text(review_frame, width=40, height=7)
        self.review_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Scrollbar for review entry
        scrollbar = tk.Scrollbar(review_frame, orient=tk.VERTICAL, command=self.review_entry.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.review_entry.config(yscrollcommand=scrollbar.set)

        # Initialize SentimentIntensityAnalyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

        # Real-time analysis checkbutton
        self.real_time_var = tk.BooleanVar(value=False)  # Default: Real-time analysis enabled
        self.real_time_checkbutton = tk.Checkbutton(master, text="Enable Real-Time Analysis", variable=self.real_time_var, command=self.toggle_real_time, bg=self.bg_color, fg=self.text_color)
        self.real_time_checkbutton.pack()

        # Frame for buttons
        button_frame = tk.Frame(master, bg=self.bg_color)
        button_frame.pack(pady=5)

        # Analyze, clear, load, word count, and pie chart buttons
        self.analyze_button = tk.Button(button_frame, text="Analyze", command=self.analyze_review, bg=self.button_bg_color, fg=self.button_fg_color)
        self.analyze_button.grid(row=0, column=0, padx=5)
        self.word_cloud_button = tk.Button(button_frame, text="Word Cloud", command=self.display_word_cloud, bg=self.button_bg_color, fg=self.button_fg_color)
        self.word_cloud_button.grid(row=0, column=1, padx=5)
        self.pie_chart_button = tk.Button(button_frame, text="Pie Chart", command=self.display_pie_chart, bg=self.button_bg_color, fg=self.button_fg_color)
        self.pie_chart_button.grid(row=0, column=2, padx=5)
        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_text, bg=self.button_bg_color, fg=self.button_fg_color)
        self.clear_button.grid(row=0, column=3, padx=5)

        # Frame for result display
        result_frame = tk.Frame(master, bd=2, relief=tk.GROOVE, bg=self.bg_color)
        result_frame.pack(pady=10)

        # Text widget to display sentiment result
        self.result_text = tk.Text(result_frame, height=10, width=50)
        self.result_text.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Scrollbar for result_text
        scrollbar = tk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)

        # Label for word count
        self.word_count_label = tk.Label(master, text="Word Count: 0", bg=self.bg_color, fg=self.text_color)
        self.word_count_label.pack()

        # Load pre-trained model and tokenizer
        saved_model_path = r"C:\Users\AQII\Final Project\FYP\saved2"
        self.model = AutoModelForSequenceClassification.from_pretrained(saved_model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(saved_model_path)

        # Configure GUI styling
        self.configure_gui_styling()

    def toggle_real_time(self):
        """Toggle real-time analysis based on the checkbutton state."""
        if self.real_time_var.get():
            self.review_entry.bind("<KeyRelease>", self.analyze_real_time)
        else:
            self.review_entry.unbind("<KeyRelease>")

    def analyze_real_time(self, event=None):
        """Perform sentiment analysis in real-time as the user types."""
        review_text = self.review_entry.get("1.0", "end-1c").strip()

        if review_text:
            # Perform sentiment analysis
            sentiment_scores = self.sentiment_analyzer.polarity_scores(review_text)
            compound_score = sentiment_scores['compound']
            sentiment = "Positive" if compound_score >= 0.05 else "Negative" if compound_score <= -0.05 else "Neutral"

            # Update display with real-time sentiment analysis
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", "end")
            self.result_text.insert(
                "1.0",
                f"Sentiment Analysis:\nCompound Score: {compound_score:.2f}\nOverall Sentiment: {sentiment}\n\n"
            )
            self.result_text.config(state="disabled")

    def configure_gui_styling(self):
        """Configure consistent GUI styling."""
        font = ("Arial", 12)
        self.analyze_button.config(font=font)
        self.word_cloud_button.config(font=font)
        self.pie_chart_button.config(font=font)
        self.clear_button.config(font=font)

    def analyze_review(self):
        """Analyze the sentiment of the entered review."""
        review_text = self.review_entry.get("1.0", "end-1c")  # Get text from Text widget

        if review_text.strip() == "":
            messagebox.showerror("Error", "Please enter a review.")
            return

        # Tokenize the review
        encoded_review = self.tokenizer(review_text, padding=True, truncation=True, max_length=512, return_tensors="pt")

        # Perform sentiment analysis
        with torch.no_grad():
            output = self.model(**encoded_review)
            prediction = torch.softmax(output.logits, dim=1)
            sentiment = torch.argmax(prediction, dim=1).item()

        # Calculate scores
        positive_score = prediction[0][1].item()
        negative_score = prediction[0][0].item()
        neutral_score = 1 - positive_score - negative_score

        # Calculate percentages
        positive_percentage = positive_score * 100
        negative_percentage = negative_score * 100
        neutral_percentage = neutral_score * 100
        compound_percentage = positive_percentage - negative_percentage

        # Display sentiment result
        self.display_sentiment_result(compound_percentage, positive_percentage, negative_percentage, neutral_percentage)

    def clear_text(self):
        """Clear the review entry and result text."""
        confirmation = messagebox.askyesno("Clear Text", "Are you sure you want to clear the text?")
        if confirmation:
            self.review_entry.delete("1.0", "end")  # Clear Text widget
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", "end")
            self.result_text.config(state="disabled")

    def load_text_file(self):
        """Load text from a file."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
                self.review_entry.delete("1.0", "end")
                self.review_entry.insert("1.0", text)
                self.update_word_count()  # Update word count after loading text

    def display_sentiment_result(self, compound_score, positive_score, negative_score, neutral_score):
        """Display the sentiment analysis result."""
        sentiment = "Positive" if compound_score >= 0.05 else "Negative" if compound_score <= -0.05 else "Neutral"

        # Display sentiment result
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert(
            "1.0",
            f"Sentiment Analysis:\nCompound Score: {compound_score:.2f}%\nPositive Score: {positive_score:.2f}%\nNegative Score: {negative_score:.2f}%\nNeutral Score: {neutral_score:.2f}%\nOverall Sentiment: {sentiment}\n\n"
        )

        explanation = "Sentiment Explanation:\n"
        explanation += "The compound score quantifies the overall sentiment. A score above 0.05 is considered positive, below -0.05 is negative, and between these values is neutral.\n\n"
        explanation += "The positive, negative, and neutral scores represent the proportion of the text that falls into each category.\n\n"
        self.result_text.insert("end", explanation)

        recommendation = "Recommendation:\n"
        if compound_score >= 0.5:
            recommendation += "The text shows strongly positive sentiment. Great job!\n"
        elif compound_score >= 0.05:
            recommendation += "The text has a positive tone.\n"
        elif compound_score <= -0.5:
            recommendation += "The text shows strongly negative sentiment. Consider revising.\n"
        elif compound_score <= -0.05:
            recommendation += "The text has a negative tone.\n"
        else:
            recommendation += "The text seems neutral in sentiment.\n"
        self.result_text.insert("end", recommendation)

        self.result_text.config(state="disabled")

    def update_word_count(self, event=None):
        """Update the word count."""
        text = self.review_entry.get("1.0", "end-1c")  # Get text from Text widget
        words = text.split()
        word_count = len(words)
        self.word_count_label.config(text=f"Word Count: {word_count}")

    def show_analysis_history(self):
        """Display the analysis history in a new window."""
        analysis_history = [("2024-02-19 14:30:00", {"positive": 0.6, "negative": 0.2, "neutral": 0.2}),
                            ("2024-02-19 15:00:00", {"positive": 0.4, "negative": 0.4, "neutral": 0.2})]

        history_window = tk.Toplevel(self.master)
        history_window.title("Analysis History")
        history_window.geometry("400x400")  # Set initial window size
        history_window.resizable(True, True)  # Make window resizable in both directions

        history_text = tk.Text(history_window, height=20, width=60)
        history_text.pack()

        # Display analysis history with timestamps
        for timestamp, scores in analysis_history:
            history_text.insert("end", f"Analysis Time: {timestamp}\n")
            for emotion, score in scores.items():
                history_text.insert("end", f"{emotion.capitalize()}: {score}\n")
            history_text.insert("end", "\n")

    def display_pie_chart(self):
        """Display a pie chart representing sentiment analysis."""
        # Function to display pie chart in a new window
        pie_chart_window = tk.Toplevel(self.master)
        pie_chart_window.title('Sentiment Analysis - Pie Chart')
    
        # Prepare data for pie chart
        text = self.review_entry.get("1.0", "end-1c")  # Get text from Text widget
        sentiment_analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = sentiment_analyzer.polarity_scores(text)

        # Calculate compound score
        compound_score = sentiment_scores['compound']

        # Determine sentiment based on compound score
        sentiment = "Positive" if compound_score >= 0.05 else "Negative" if compound_score <= -0.05 else "Neutral"

        # Display sentiment result
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert(
            "1.0",
            f"Sentiment Analysis:\nCompound Score: {compound_score:.2f}\nOverall Sentiment: {sentiment}\n\n"
        )
        self.result_text.config(state="disabled")

        # Prepare data for pie chart
        sizes = [sentiment_scores['pos'], sentiment_scores['neg'], sentiment_scores['neu']]
        labels = ['Positive', 'Negative', 'Neutral']
        explode = (0.1, 0, 0)  # To explode the first slice (if desired)
        colors = ['#4CAF50', '#F44336', '#FFC107']

        # Plotting the pie chart with enhanced settings
        fig, ax = plt.subplots(figsize=(6, 5))
        pie = ax.pie(
            sizes, 
            explode=explode, 
            labels=labels, 
            colors=colors, 
            autopct='%1.1f%%', 
            shadow=True, 
            startangle=140
        )

        # Capturing patches from the pie chart
        patches = pie[0]

        # Display percentage inside the pie chart segments
        for i, (label, size) in enumerate(zip(labels, sizes)):
            ax.text(
                0.5 * sizes[i] * (explode[i] + 0.1),
                0.5 * sizes[i] * explode[i],
                f'{sizes[i]:.1f}%',
                ha='center',
                va='center'
            )

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title('Sentiment Analysis - Pie Chart')

        # Add legend using the captured patches and labels
        ax.legend(patches, labels, loc="best")

        # Use mplcursors to display information on hover
        mplcursors.cursor(pie[0], hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{labels[sel.target.index]} - {sizes[sel.target.index]:.1f}%"))

        # Display the pie chart window
        canvas = FigureCanvasTkAgg(fig, master=pie_chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        plt.show()

    def display_word_cloud(self):
        """Display a word cloud representing the entered text."""
        # Get text from the entry
        text = self.review_entry.get("1.0", "end-1c")

        # Generate word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

        # Create a new window to display the word cloud
        wordcloud_window = tk.Toplevel(self.master)
        wordcloud_window.title('Word Cloud')
        wordcloud_window.geometry("600x400")  # Set initial window size
        wordcloud_window.resizable(True, True)  # Make window resizable in both directions

        # Display word cloud
        plt.figure(figsize=(8, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud')

        # Display the word cloud in the canvas
        canvas = FigureCanvasTkAgg(plt.gcf(), master=wordcloud_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
 
        # Show the word cloud window
        wordcloud_window.mainloop()

    def display_sentiment_result(self, compound_score, positive_score, negative_score, neutral_score):
        """Display the sentiment analysis result."""
        sentiment = "Positive" if compound_score >= 0.05 else "Negative" if compound_score <= -0.05 else "Neutral"

        # Display sentiment result
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert(
            "1.0",
            f"Sentiment Analysis:\nCompound Score: {compound_score:.2f}%\nPositive Score: {positive_score:.2f}%\nNegative Score: {negative_score:.2f}%\nNeutral Score: {neutral_score:.2f}%\nOverall Sentiment: {sentiment}\n\n"
        )

        explanation = "Sentiment Explanation:\n"
        explanation += "The compound score quantifies the overall sentiment. A score above 0.05 is considered positive, below -0.05 is negative, and between these values is neutral.\n\n"
        explanation += "The positive, negative, and neutral scores represent the proportion of the text that falls into each category.\n\n"
        self.result_text.insert("end", explanation)

        recommendation = "Recommendation:\n"
        if compound_score >= 0.5:
            recommendation += "The text shows strongly positive sentiment. Great job!\n"
        elif compound_score >= 0.05:
            recommendation += "The text has a positive tone.\n"
        elif compound_score <= -0.5:
            recommendation += "The text shows strongly negative sentiment. Consider revising.\n"
        elif compound_score <= -0.05:
            recommendation += "The text has a negative tone.\n"
        else:
            recommendation += "The text seems neutral in sentiment.\n"
        self.result_text.insert("end", recommendation)

        self.result_text.config(state="disabled")
        
root = tk.Tk()
app = SentimentAnalysisApp(root)
root.iconbitmap(r"C:\\Users\AQII\\Final Project\FYP\Login\favicon.ico") 

if __name__ == "__main__":
    
    firebaseConfig = {
  'apiKey': "AIzaSyCTqRX0fteJddqB2CluPZQP7QJTOuP2MJY",
  'authDomain': "nlp-fyp.firebaseapp.com",
  'databaseURL': "https://nlp-fyp-default-rtdb.firebaseio.com",
  'projectId': "nlp-fyp",
  'storageBucket': "nlp-fyp.appspot.com",
  'messagingSenderId': "471709726502",
  'appId': "1:471709726502:web:6bf14fb152c1d0ebb7f3e7"
}

    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    # Start the main application
    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("blue")

app = LoginSignupApp(auth)
root.mainloop()
