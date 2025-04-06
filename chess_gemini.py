import chess
import chess.svg
import streamlit as st
import google.generativeai as genai
import base64

# Initialize session state variables
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = None
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "made_move" not in st.session_state:
    st.session_state.made_move = False
if "board_svg" not in st.session_state:
    st.session_state.board_svg = None
if "move_history" not in st.session_state:
    st.session_state.move_history = []
if "max_turns" not in st.session_state:
    st.session_state.max_turns = 5

st.sidebar.title("Chess Agent Configuration")

# Get API Key from user with a generic label
gemini_api_key = st.sidebar.text_input("Enter your Gemini API key", type="password")
if gemini_api_key:
    st.session_state.gemini_api_key = gemini_api_key
    genai.configure(api_key=gemini_api_key)
    st.sidebar.success("API key saved!")

st.sidebar.info("""
For a complete chess game with potential checkmate, max_turns may need to be > 200.
However, this will consume significant API credits and time.
For demo purposes, 5-10 turns is recommended.
""")

max_turns_input = st.sidebar.number_input(
    "Enter the number of turns (max_turns):",
    min_value=1,
    max_value=1000,
    value=st.session_state.max_turns,
    step=1
)
st.session_state.max_turns = max_turns_input
st.sidebar.success(f"Max turns set to {st.session_state.max_turns}!")

st.title("Chess with Gemini AI")

def available_moves() -> str:
    return ", ".join(str(move) for move in st.session_state.board.legal_moves)

def execute_move(move_str: str) -> str:
    try:
        move = chess.Move.from_uci(move_str)
        if move not in st.session_state.board.legal_moves:
            error_msg = f"Invalid move: {move_str}. Available moves: {available_moves()}"
            print(error_msg)
            return error_msg
        
        st.session_state.board.push(move)
        st.session_state.made_move = True
        
        board_svg = chess.svg.board(st.session_state.board, size=400)
        st.session_state.board_svg = board_svg
        st.session_state.move_history.append(move_str)
        
        # Print move and current board state in terminal
        print(f"Move executed: {move_str}")
        print("Current Board:")
        print(st.session_state.board)
        return f"Move executed: {move_str}"
    except ValueError:
        error_msg = "Invalid move format. Use UCI notation (e.g., 'e2e4')."
        print(error_msg)
        return error_msg

def get_ai_move():
    if not st.session_state.gemini_api_key:
        error_msg = "No API key provided. Please enter your Gemini API key."
        print(error_msg)
        return error_msg
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"You are playing chess as {'White' if st.session_state.board.turn == chess.WHITE else 'Black'}.\n"
        f"Board FEN: {st.session_state.board.fen()}\n"
        f"Available moves: {available_moves()}\n"
        "Choose the best move in UCI format (e.g., 'e2e4')."
    )

    print("Prompt sent to AI:")
    print(prompt)
    
    response = model.generate_content(prompt)
    if response and hasattr(response, 'text'):
        ai_move = response.text.strip()
        print(f"AI generated move: {ai_move}")
        # Validate by converting to a move
        try:
            move = chess.Move.from_uci(ai_move)
            if move in st.session_state.board.legal_moves:
                return ai_move
            else:
                error_msg = "Invalid AI move generated."
                print(error_msg)
                return error_msg
        except ValueError:
            error_msg = "Invalid AI move format."
            print(error_msg)
            return error_msg
    
    error_msg = "Error: AI failed to generate a valid move."
    print(error_msg)
    return error_msg

def render_svg(svg_str: str):
    """Render SVG string in Streamlit."""
    b64 = base64.b64encode(svg_str.encode("utf-8")).decode("utf-8")
    html = f'<img src="data:image/svg+xml;base64,{b64}" width="400"/>'
    st.markdown(html, unsafe_allow_html=True)

if st.button("Start AI Game"):
    if not st.session_state.gemini_api_key:
        st.error("Please enter a valid Gemini API key in the sidebar.")
    else:
        st.session_state.board.reset()
        st.session_state.move_history = []
        st.session_state.board_svg = chess.svg.board(st.session_state.board, size=400)
        render_svg(st.session_state.board_svg)
        print("Game started. Initial Board:")
        print(st.session_state.board)

        for turn in range(st.session_state.max_turns):
            print(f"\nTurn {turn+1}:")
            ai_move = get_ai_move()
            if "Invalid" in ai_move or "Error" in ai_move:
                st.write(ai_move)
                break

            move_result = execute_move(ai_move)
            # Added print statement to log each move with its turn number
            print(f"Turn {turn+1}: AI played {ai_move}")
            st.write(f"AI Move: {ai_move} -> {move_result}")
            render_svg(st.session_state.board_svg)
            if st.session_state.board.is_game_over():
                st.write("Game over!")
                print("Game over!")
                break

if st.button("Reset Game"):
    st.session_state.board.reset()
    st.session_state.move_history = []
    st.session_state.board_svg = chess.svg.board(st.session_state.board, size=400)
    st.write("Game reset! Click 'Start AI Game' to play.")
    render_svg(st.session_state.board_svg)
    print("Game reset. Initial Board:")
    print(st.session_state.board)
