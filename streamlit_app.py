import random
import streamlit as st
import operator
import time

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        body {
            background-color: #F0F8FF;  # Example background color
            /* Or use an image or gradient as background */
            /* background-image: url('https://your-image-url.com/image.jpg'); */
            /* background: linear-gradient(to right, #ff7e5f, #feb47b); */
            background-size: cover;
            background-position: center center;
        }

        .title {
            color: #FF4B4B;
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            animation: bounce 1s infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        .question {
            font-size: 30px;
            font-weight: bold;
            text-align: center;
            color: #333;
        }

        .score {
            background: #FFDDC1;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():

    st.markdown(
        '<h1 class="title">Welcome To Little Professor!!! 🎓</h1>',
        unsafe_allow_html=True,
    )

    if "score_counter" not in st.session_state:
        st.session_state.score_counter = 0
    if "main_counter" not in st.session_state:
        st.session_state.main_counter = 0
    if "mistakes" not in st.session_state:
        st.session_state.mistakes = 0
    if "score_counter" not in st.session_state:
        st.session_state.score_counter = 0
    if "main_counter" not in st.session_state:
        st.session_state.main_counter = 0
    if "mistakes" not in st.session_state:
        st.session_state.mistakes = 0
    if "current_a" not in st.session_state:
        st.session_state.current_a = 0
    if "current_b" not in st.session_state:
        st.session_state.current_b = 0
    if "current_op" not in st.session_state:
        st.session_state.current_op = None
    if "reset_input" not in st.session_state:
        st.session_state.reset_input = False
    if "error_message" not in st.session_state:
        st.session_state.error_message = None
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = None

    ops = {
        "+": operator.add,
        "-": operator.sub,
        "×": operator.mul,
    }

    if "level" not in st.session_state or st.session_state.level is None:
        get_level()
        return

    Total_score = 10 - st.session_state.score_counter

    if st.session_state.main_counter < 10:
        st.write(f"Question {st.session_state.main_counter + 1} of 10")
        progress = st.progress(st.session_state.main_counter / 10)

    else:
        if Total_score > 7:
            st.write("Good Job!!")

        elif 4 < Total_score < 8:
            st.write("Make sure not to miss your maths class!")
        else:
            st.write("You dummy")

    if st.session_state.main_counter >= 10:
        with st.container():
            col1, col2, col3 = st.columns(3)
            col1.markdown(
                f'<div class="score">✅ Correct: {10 - st.session_state.score_counter}</div>',
                unsafe_allow_html=True,
            )
            col2.markdown(
                f'<div class="score">❌ Mistakes: {st.session_state.score_counter}</div>',
                unsafe_allow_html=True,
            )
            col3.markdown(
                f'<div class="score">🎯 Total Questions: {st.session_state.main_counter}/10</div>',
                unsafe_allow_html=True,
            )

        if st.button("🔄 Play Again"):

            st.session_state.score_counter = 0
            st.session_state.mistakes = 0
            st.session_state.main_counter = 0
            st.session_state.level = None
            st.rerun()
        return

    if "question_change" not in st.session_state or st.session_state.question_change:

        st.session_state.current_op = random.choice(list(ops.keys()))
        st.session_state.current_a = generate_integer(st.session_state.level)
        st.session_state.current_b = generate_integer(st.session_state.level)
        st.session_state.question_change = False

    st.markdown(
        f'<h3 class="question">{st.session_state.current_a} {st.session_state.current_op} {st.session_state.current_b} = ?</h3>',
        unsafe_allow_html=True,
    )
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
    if st.session_state.show_answer:
        st.error(st.session_state.show_answer)

    input_key = (
        f"answer_input_{st.session_state.main_counter}_{st.session_state.mistakes}"
    )

    if st.session_state.reset_input:
        st.session_state[input_key] = ""
        st.session_state.reset_input = False

    user_input = st.text_input("Your answer:", key=input_key)
    if user_input:
        try:
            user_answer = int(user_input)
            correct_answer = ops[st.session_state.current_op](
                st.session_state.current_a, st.session_state.current_b
            )

            if user_answer == correct_answer:
                st.balloons()
                st.markdown("Correct")
                time.sleep(1)
                st.success("Next Question!")
                st.session_state.main_counter += 1
                st.session_state.mistakes = 0
                st.session_state.question_change = True
                st.session_state.reset_input = True
                st.session_state.error_message = None
                st.session_state.show_answer = None
                st.rerun()

            else:
                st.session_state.error_message = "❌ Oops! Try again."
                st.session_state.mistakes += 1
                time.sleep(1)
                st.session_state.reset_input = True
                st.session_state.show_answer = None

                if st.session_state.mistakes == 3:
                    st.session_state.show_answer = (
                        f"#### The correct answer was {correct_answer}"
                    )

                    st.session_state.score_counter += 1
                    st.session_state.main_counter += 1
                    st.session_state.mistakes = 0
                    st.session_state.question_change = True
                    st.session_state.error_message = None
                    st.session_state.reset_input = True
                    st.rerun()

                st.rerun()
        except ValueError:
            st.error("Please Input only a number")


def get_level():

    st.write("## Select Your Level")

    if "level" not in st.session_state:
        st.session_state.level = None

    col1, col2, col3 = st.columns(3)

    if col1.button("🐣 Beginner", key="lvl1_btn"):
        st.session_state.level = 1
        st.rerun()
    if col2.button("🚀 Intermediate", key="lvl2_btn"):
        st.session_state.level = 2
        st.rerun()
    if col3.button("🤓 Advanced", key="lvl3_btn"):
        st.session_state.level = 3
        st.rerun()


def generate_integer(level):
    if level == 1:
        return random.randint(1, 9)
    elif level == 2:
        return random.randint(10, 99)
    elif level == 3:
        return random.randint(100, 999)
    else:
        return random.randint(0, 9)


if __name__ == "__main__":
    main()
