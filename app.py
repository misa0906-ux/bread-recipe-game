import random
import streamlit as st

# 1. 페이지 설정 및 상단 제목/안내 문구
st.set_page_config(page_title="달콤달콤 빵 만들기 게임", page_icon="🥐")
st.title("🥐 달콤달콤 전설의 빵 만들기 게임 🥖")
st.info(
    "환영합니다! 아래 레시피 순서를 잘 기억해서 맛있는 빵을 완성해 보세요. 순서를 틀리면 처음부터 다시 시작해야 합니다!"
)


# 2. 레시피를 def 함수로 저장
def get_recipe():
    return ["반죽하기", "발효하기", "모양 맞추기", "굽기"]


recipe = get_recipe()

# 화면에 레시피 띄우기
st.subheader("📜 [레시피]")
cols = st.columns(len(recipe))
for idx, step in enumerate(recipe):
    cols[idx].markdown(f"**{idx + 1}. {step}**")

st.divider()

# 게임 상태(Session State) 초기화
if "history" not in st.session_state:
    st.session_state.history = []  # 여태까지 했던 공정을 저장할 list
if "step_idx" not in st.session_state:
    st.session_state.step_idx = 0  # 현재 진행 중인 단계 인덱스 (0~3)
if "choices" not in st.session_state:
    # random 모듈을 사용해 선택지 순서를 무작위로 섞음
    shuffled = get_recipe()
    random.shuffle(shuffled)
    st.session_state.choices = shuffled
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# 3. 사용자 입력 받기 (선택지 + 제3의 대답을 테스트할 수 있는 직접 입력)
st.subheader(f"👉 현재 진행할 단계 ({st.session_state.step_idx + 1}단계)")

# random으로 섞인 선택지 표시
st.write("🔀 **오늘의 무작위 작업대(선택지):**", " | ".join(st.session_state.choices))

with st.form(key="baking_form", clear_on_submit=True):
    user_input = st.text_input(
        "수행할 공정을 입력하세요 (예: 반죽하기, 발효하기, 모양 맞추기, 굽기):",
        placeholder="여기에 공정을 입력하고 '실행하기'를 누르세요!",
    )
    submit_btn = st.form_submit_button("실행하기 👩‍🍳")

# 4. while 무한 반복 및 if-elif-else 로직 처리
if submit_btn and not st.session_state.game_over:
    # Streamlit의 무한 로딩 방지를 위해, 입력값이 들어왔을 때 while 루프로 검증 후 break
    while True:
        clean_input = user_input.strip()
        correct_step = recipe[st.session_state.step_idx]

        # 조건 1: 제 3의 대답을 한 경우 (레시피에 없는 단어 입력)
        if clean_input not in recipe:
            st.warning(
                f"⚠️ '{clean_input}'은(는) 레시피에 없는 제3의 행동입니다! 보기에 있는 공정을 다시 입력해 주세요."
            )
            break

        # 조건 2: 알맞게 답한 경우
        elif clean_input == correct_step:
            st.session_state.history.append(clean_input)  # list에 성공한 공정 저장
            st.session_state.step_idx += 1

            # 선택지 다시 랜덤하게 섞기
            random.shuffle(st.session_state.choices)

            # 모든 단계를 맞게 끝낸 경우
            if st.session_state.step_idx == len(recipe):
                st.balloons()
                st.success(
                    "🎉 **성공!** 완벽한 순서로 맛있는 빵을 구워냈습니다!"
                )
                st.write(
                    "✅ **완성까지 진행한 공정 기록 (list):**",
                    st.session_state.history,
                )
                st.session_state.game_over = True
            else:
                st.success(
                    f"⭕ 정답입니다! '{clean_input}' 완료! 다음 단계로 넘어갑니다."
                )
            break

        # 조건 3: 레시피에 있는 단어지만 잘못된 단계를 입력한 경우
        else:
            st.error("💥 **실패!** 잘못된 순서로 작업을 진행해서 반죽을 망쳤습니다.")

            # 틀린 단계를 Metric으로 강조
            st.metric(
                label="🚨 실수한 공정 (틀린 단계)",
                value=clean_input,
                delta=f"원래 필요한 단계: {correct_step}",
                delta_color="inverse",
            )

            # 여태까지 했던 공정을 list로 보여주기
            st.write(
                "📋 **실패 전까지 진행했던 공정 (list):**",
                st.session_state.history,
            )
            st.info("🔄 처음(1단계)부터 다시 시작합니다!")

            # 처음으로 초기화
            st.session_state.history = []
            st.session_state.step_idx = 0
            random.shuffle(st.session_state.choices)
            break

# 현재까지 성공한 공정 실시간 표시
if st.session_state.history and not st.session_state.game_over:
    st.caption(f"현재까지 완료된 공정: {st.session_state.history}")

# 다시하기 버튼 (게임 성공 시)
if st.session_state.game_over:
    if st.button("새 빵 만들기 (처음부터 다시하기) 🔄"):
        st.session_state.history = []
        st.session_state.step_idx = 0
        st.session_state.game_over = False
        random.shuffle(st.session_state.choices)
        st.rerun()
