from shiny import App, reactive, render, ui
from datetime import datetime
import duckdb

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h3("Sign the Guestbook"),
        ui.input_text("name", "Your Name", placeholder="Enter your name"),
        ui.input_text_area("comment", "Your Comment", placeholder="Leave a message"),
        ui.input_action_button("submit", "Submit", class_="btn-primary"),
        ui.hr(),
        ui.p("Fill in your name and comment, then click Submit to add your message to the guestbook."),
    ),
    ui.card(
        ui.h2("Guestbook Entries"),
        ui.output_ui("entries"),
    ),
)

def server(input, output, session):
    # Initialize database connection
    con = duckdb.connect(':memory:')
    
    # Create the table if it doesn't exist
    con.execute("""
        CREATE TABLE IF NOT EXISTS guestbook (
            name VARCHAR,
            comment VARCHAR,
            datetime TIMESTAMP
        )
    """)
    
    # Insert some initial sample data
    con.execute("""
        INSERT INTO guestbook VALUES 
        ('Alice', 'First post!', '2024-01-01 10:00:00'),
        ('Bob', 'Great guestbook app!', '2024-01-01 10:05:00')
    """)
    
    # Function to get all entries
    def get_entries():
        return con.execute("""
            SELECT name, comment, datetime 
            FROM guestbook 
            ORDER BY datetime DESC
        """).fetchall()
    
    # Store entries in a reactive value
    entries_rv = reactive.value(get_entries())
    
    @reactive.effect
    @reactive.event(input.submit)
    def add_entry():
        # Only add entry if both name and comment are provided
        if input.name().strip() and input.comment().strip():
            # Insert new entry into database
            con.execute("""
                INSERT INTO guestbook (name, comment, datetime)
                VALUES (?, ?, ?)
            """, [input.name(), input.comment(), datetime.now()])
            
            # Update reactive value with fresh data from database
            entries_rv.set(get_entries())
            
            # Clear the inputs
            ui.update_text("name", value="")
            ui.update_text("comment", value="")

    @render.ui
    def entries():
        current_entries = entries_rv()
        if not current_entries:
            return ui.p("No entries yet. Be the first to sign!")
        
        # Create a list of entries
        entry_list = []
        for entry in current_entries:
            entry_list.append(
                ui.div(
                    ui.h4(entry[0]),  # name
                    ui.p(entry[1]),   # comment
                    ui.p(
                        str(entry[2]),  # datetime
                        style="color: #666; font-size: 0.8em;"
                    ),
                    ui.hr(),
                )
            )
        return ui.div(*entry_list)

app = App(app_ui, server)
