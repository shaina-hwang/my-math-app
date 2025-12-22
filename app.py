import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px
from streamlit_drawable_canvas import st_canvas

# --- 1. 페이지 및 테마 설정 ---
st.set_page_config(page_title="2025 AI 수학 마스터", layout="wide", initial_sidebar_state="expanded")

# --- 2. 문제 생성 로직 (확장형) ---
import random
import math

def generate_problem(level, unit):
    """
    바다코끼리 연산자(:=)를 전혀 사용하지 않는 표준 방식으로,
    모든 파이썬 버전에서 오류 없이 작동하는 무한 문제 생성기입니다.
    """
    
    # --- 1. 초등학교 과정 ---
    if "초등학교" in level:
        if unit == "수와 연산":
            def q1():
                a, b = random.randint(100, 999), random.randint(100, 999)
                return f"{a} + {b} = ?", str(a + b)
            def q2():
                a = random.randint(500, 999)
                b = random.randint(100, a)
                return f"{a} - {b} = ?", str(a - b)
            def q3():
                a, b = random.randint(11, 99), random.randint(2, 9)
                return f"{a} × {b} = ?", str(a * b)
            def q4():
                b = random.randint(2, 9)
                c = random.randint(11, 50)
                a = b * c
                return f"{a} ÷ {b} = ?", str(c)
            def q5():
                d = random.randint(5, 12)
                n = random.randint(1, d-2)
                return f"분모가 {d}인 분수 {n}/{d} + 1/{d} = ?", f"{n+1}/{d}"
            return random.choice([q1, q2, q3, q4, q5])()

        elif unit == "도형":
            def q1():
                s = random.randint(2, 15)
                return f"한 변이 {s}cm인 정사각형의 둘레는? (cm)", str(s * 4)
            def q2():
                r = random.randint(2, 10)
                return f"반지름이 {r}cm인 원의 지름은? (cm)", str(r * 2)
            return random.choice([q1, q2])()

        elif unit == "측정":
            def q1():
                h, m = random.randint(1, 5), random.randint(1, 59)
                return f"{h}시간 {m}분은 총 몇 분인가요?", str(h * 60 + m)
            def q2():
                kg = random.randint(1, 10)
                return f"{kg}kg은 몇 g인가요?", str(kg * 1000)
            return random.choice([q1, q2])()

        elif "규칙" in unit:
            s, g = random.randint(1, 5), random.randint(2, 5)
            return f"{s}, {s+g}, {s+g*2}, {s+g*3}... 이 규칙에서 5번째 숫자는?", str(s + g * 4)
        
        else: # 자료와 가능성
            a, b, c = random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)
            return f"세 수 {a}, {b}, {c}의 합계는?", str(a + b + c)

    # --- 2. 중학교 과정 ---
    elif "중학교" in level:
        if unit == "수와 연산":
            def q1():
                n = random.randint(11, 19)
                return f"{n}의 제곱( {n}² )의 값은?", str(n**2)
            def q2():
                n = random.randint(2, 20)
                return f"√{n*n} 의 값은?", str(n)
            return random.choice([q1, q2])()

        elif unit == "문자와 식":
            x = random.randint(1, 10)
            a, b = random.randint(2, 6), random.randint(1, 15)
            c = a * x + b
            return f"{a}x + {b} = {c} 일 때, x는?", str(x)

        elif unit == "함수":
            a, x = random.randint(2, 5), random.randint(1, 4)
            return f"y = {a}x 그래프가 점({x}, k)를 지날 때 k는?", str(a * x)

        elif unit == "도형":
            return "밑변 6, 높이 8인 직각삼각형의 빗변 길이는?", "10"

        else: # 확률과 통계
            return "동전 한 개를 던질 때 앞면이 나올 확률은? (분수로)", "1/2"

    # --- 3. 고등학교 과정 ---
    else:
        if "수학 I" in unit:
            exp = random.randint(1, 4)
            val = 3 ** exp
            return f"log3({val})의 값은?", str(exp)
        elif "수학 II" in unit:
            n = random.randint(2, 4)
            return f"f(x) = x^{n} 일 때 f'(1)의 값은?", str(n)
        elif "미적분" in unit:
            return "sin(x)를 x에 대해 미분하면? (소문자)", "cos(x)"
        elif "확률" in unit:
            n = random.randint(4, 6)
            res = math.comb(n, 2)
            return f"{n}명 중 2명을 뽑는 조합({n}C2)의 수는?", str(res)
        else: # 기하
            return "벡터의 크기가 1인 벡터를 무엇이라 하나요?", "단위벡터"

    return "문제를 생성 중입니다.", "0"



# --- 3. 세션 상태 관리 ---
if 'history' not in st.session_state: st.session_state.history = []
if 'current_problem' not in st.session_state: st.session_state.current_problem = None
if 'submitted' not in st.session_state: st.session_state.submitted = False
if 'last_unit' not in st.session_state: st.session_state.last_unit = None
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()

# --- 4. 사이드바: 설정 및 배지 시스템 ---
st.sidebar.header("🎓 학습 설정")
levels = ["초등학교 (기초 다지기)", "중학교 (개념 확장)", "고등학교 (추상화 및 심화)"]
units = {
    levels[0]: ["수와 연산", "도형", "측정", "규칙성", "자료와 가능성"],
    levels[1]: ["수와 연산", "문자와 식", "함수", "도형", "확률과 통계"],
    levels[2]: ["수학 I (공통)", "수학 II (공통)", "미적분", "확률과 통계", "기하"]
}

level = st.sidebar.selectbox("교육과정 선택", levels)
unit = st.sidebar.selectbox("단원 선택", units[level])

# [자동 변경 로직] 단원 선택 즉시 새 문제 생성
if unit != st.session_state.last_unit:
    st.session_state.current_problem = generate_problem(level, unit)
    st.session_state.submitted = False
    st.session_state.last_unit = unit

if st.sidebar.button("다른 숫자 문제 생성"):
    st.session_state.current_problem = generate_problem(level, unit)
    st.session_state.submitted = False
    st.rerun()

# 게이미피케이션: 배지 시스템
correct_total = sum(1 for x in st.session_state.history if x['결과'])
st.sidebar.markdown("---")
st.sidebar.subheader("🏅 나의 배지")
if correct_total >= 1: st.sidebar.write("🌱 수학 새싹 (1문제 성공)")
if correct_total >= 5: st.sidebar.write("🌿 수학 유망주 (5문제 성공)")
if correct_total >= 10: st.sidebar.write("🔥 수학 전사 (10문제 성공)")

# --- 5. 메인 화면: 문제 및 타이머 ---
from streamlit_autorefresh import st_autorefresh

# 1초마다 앱을 재실행하여 타이머를 갱신합니다.
st_autorefresh(interval=1000, key="timer_refresh")

if unit != st.session_state.last_unit:
    st.session_state.current_problem = generate_problem(level, unit)
    st.session_state.submitted = False
    st.session_state.last_unit = unit
    st.session_state.start_time = time.time()

st.title(f"✍️ {unit} 집중 학습")

# 실시간 시간 계산
elapsed_time = int(time.time() - st.session_state.start_time)

# 타이머 표시 (제출 전에는 실시간 초, 제출 후에는 결과 시간 고정)
st.caption(f"⏱️ 공부 시간: {elapsed_time}초 경과")

col_quiz, col_canvas = st.columns([1, 1])

with col_quiz:
    if st.session_state.current_problem:
        q, a = st.session_state.current_problem
        st.info(f"**문제:** {q}")
        
        with st.form("quiz_form"):
            # 제출된 상태라면 입력창을 비활성화합니다.
            user_ans = st.text_input("정답 입력", disabled=st.session_state.submitted)
            
            # 제출된 상태라면 '제출' 버튼을 비활성화합니다.
            btn = st.form_submit_button("제출 및 결과 확인", disabled=st.session_state.submitted)
            
            if btn and user_ans:
                # [중요] 이미 제출된 상태라면 아무것도 하지 않습니다 (중복 클릭 방지)
                if not st.session_state.submitted:
                    st.session_state.submitted = True
                    is_correct = (user_ans.strip() == a)
                    
                    # 기록은 한 번만 추가됩니다.
                    st.session_state.history.append({
                        "과정": level, "단원": unit, "문제": q, "정답": a, 
                        "내 답": user_ans, "결과": is_correct
                    })
                    st.rerun()

        # 결과 메시지 표시
        if st.session_state.submitted:
            res = st.session_state.history[-1]
            if res["결과"]:
                st.success(f"정답입니다!")
            else:
                st.error(f"오답입니다. 정답은 {a}입니다.")
                with st.expander("🤖 AI 튜터의 쉬운 풀이"):
                    st.write(f"이 문제는 **{unit}**의 기본 원리를 묻고 있어요.")
                    st.write(f"정답인 {a}가 나오기 위해서는 단계별로 이렇게 생각해보세요...")


with col_canvas:
    st.write("🎨 **그림 연습장**")
    # key값에 현재 시간을 포함하지 않아야 새로고침 시에도 그림이 유지됩니다.
    st_canvas(stroke_width=2, stroke_color="#212121", background_color="#FFFFFF", 
              height=350, key=f"canv_{unit}_{st.session_state.current_problem}")
    if st.button("다른 문제 도전"):
        st.session_state.current_problem = generate_problem(level, unit)
        st.session_state.submitted = False

# --- 6. 오답 노트 섹션 ---
st.divider()

if st.session_state.history:
    st.header("📝 나의 오답 노트")
    df = pd.DataFrame(st.session_state.history)
    
    # 결과가 False인 데이터만 추출
    wrong_df = df[df["결과"] == False]
    
    if not wrong_df.empty:
        # 탭 없이 바로 테이블로 깔끔하게 표시 (통계 삭제 버전)
        st.write("틀린 문제들을 복습해보세요.")
        # "내답"에 띄어쓰기가 없는지 다시 확인하세요.
        st.table(wrong_df[["단원", "문제", "내 답", "정답"]])
    else:
        st.success("현재까지 오답이 없습니다. 정말 대단해요! 🌟")
else:
    st.info("문제를 풀면 오답 기록이 여기에 표시됩니다.")
