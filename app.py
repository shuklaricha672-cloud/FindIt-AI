import streamlit as st
import os

from PIL import Image

from database.database import (
    create_database,
    add_item,
    get_items
)

from ai.detector import detect_objects

from ai.matcher import calculate_match

from utils.helpers import save_uploaded_file


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="FindIt AI",
    page_icon="🔎",
    layout="wide"
)


# ==========================================
# DATABASE
# ==========================================

create_database()


# ==========================================
# HEADER
# ==========================================

st.title("🔎 FindIt AI")

st.subheader(
    "AI Powered Smart Lost & Found System"
)

st.write(
    "Find your lost belongings using AI-powered "
    "object detection and smart matching."
)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📌 Menu")

page = st.sidebar.radio(
    "Select Option",
    [
        "🏠 Home",
        "📢 Report Lost Item",
        "📦 Report Found Item",
        "🔍 Find My Item",
        "📋 All Items"
    ]
)


# ==========================================
# HOME
# ==========================================

if page == "🏠 Home":

    st.header("Welcome to FindIt AI 🚀")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🤖 AI Detection",
            "YOLO"
        )

    with col2:
        st.metric(
            "🔍 Smart Matching",
            "AI"
        )

    with col3:
        st.metric(
            "🗄️ Database",
            "SQLite"
        )

    st.success(
        "Lost something? Let AI help you find it!"
    )

    st.markdown("""
    ### How it works?

    1. 📸 Upload lost item photo
    2. 🤖 AI identifies the object
    3. 🔎 System searches found items
    4. 📊 Matching score is calculated
    5. 🎯 Possible matches are displayed
    """)


# ==========================================
# REPORT LOST ITEM
# ==========================================

elif page == "📢 Report Lost Item":

    st.header("📢 Report Lost Item")

    item_type = st.selectbox(
        "Item Category",
        [
            "person",
            "backpack",
            "laptop",
            "cell phone",
            "bottle",
            "book",
            "wallet",
            "watch",
            "headphones",
            "keys",
            "other"
        ]
    )

    description = st.text_area(
        "Describe your lost item"
    )

    location = st.selectbox(
        "Where did you lose it?",
        [
            "Library",
            "Canteen",
            "Classroom",
            "Computer Lab",
            "Parking",
            "Playground",
            "Auditorium",
            "Other"
        ]
    )

    contact = st.text_input(
        "Contact Information"
    )

    image = st.file_uploader(
        "Upload Item Photo",
        type=["jpg", "jpeg", "png"]
    )

    if st.button("🚨 Report Lost Item"):

        if image is None:

            st.error(
                "Please upload an image."
            )

        elif not contact:

            st.error(
                "Please enter contact information."
            )

        else:

            file_path = save_uploaded_file(
                image,
                "data/lost_items"
            )

            add_item(
                item_type,
                description,
                location,
                "LOST",
                file_path,
                contact
            )

            st.success(
                "✅ Lost item reported successfully!"
            )


# ==========================================
# REPORT FOUND ITEM
# ==========================================

elif page == "📦 Report Found Item":

    st.header("📦 Report Found Item")

    item_type = st.selectbox(
        "Item Category",
        [
            "person",
            "backpack",
            "laptop",
            "cell phone",
            "bottle",
            "book",
            "wallet",
            "watch",
            "headphones",
            "keys",
            "other"
        ],
        key="found_type"
    )

    description = st.text_area(
        "Describe the found item"
    )

    location = st.selectbox(
        "Where did you find it?",
        [
            "Library",
            "Canteen",
            "Classroom",
            "Computer Lab",
            "Parking",
            "Playground",
            "Auditorium",
            "Other"
        ],
        key="found_location"
    )

    contact = st.text_input(
        "Your Contact Information"
    )

    image = st.file_uploader(
        "Upload Found Item Photo",
        type=["jpg", "jpeg", "png"],
        key="found_image"
    )

    if st.button("📦 Report Found Item"):

        if image is None:

            st.error(
                "Please upload an image."
            )

        elif not contact:

            st.error(
                "Please enter contact information."
            )

        else:

            file_path = save_uploaded_file(
                image,
                "data/found_items"
            )

            add_item(
                item_type,
                description,
                location,
                "FOUND",
                file_path,
                contact
            )

            st.success(
                "✅ Found item reported successfully!"
            )


# ==========================================
# FIND MY ITEM
# ==========================================

elif page == "🔍 Find My Item":

    st.header("🔍 Find My Lost Item")

    uploaded_image = st.file_uploader(
        "Upload your lost item's photo",
        type=["jpg", "jpeg", "png"],
        key="search_image"
    )

    location = st.selectbox(
        "Where did you lose it?",
        [
            "Library",
            "Canteen",
            "Classroom",
            "Computer Lab",
            "Parking",
            "Playground",
            "Auditorium",
            "Other"
        ],
        key="search_location"
    )

    description = st.text_area(
        "Describe your lost item",
        key="search_description"
    )

    if uploaded_image:

        image = Image.open(
            uploaded_image
        )

        st.image(
            image,
            caption="Your Lost Item",
            width=300
        )

        if st.button("🤖 Find Matching Items"):

            with st.spinner(
                "AI is analyzing your image..."
            ):

                detected_objects = detect_objects(
                    image
                )

            # -----------------------------
            # AI DETECTION
            # -----------------------------

            st.subheader(
                "🤖 AI Detected Objects"
            )

            if detected_objects:

                for obj in detected_objects:

                    st.write(
                        f"🔹 {obj['name']} "
                        f"— {obj['confidence']}%"
                    )

            else:

                st.warning(
                    "No recognizable object detected."
                )

            # -----------------------------
            # FIND FOUND ITEMS
            # -----------------------------

            found_items = get_items("FOUND")

            st.subheader(
                "🎯 Possible Matches"
            )

            if not found_items:

                st.info(
                    "No found items have been reported yet."
                )

            else:

                matches = []

                for item in found_items:

                    (
                        item_id,
                        found_type,
                        found_description,
                        found_location,
                        status,
                        image_path,
                        contact,
                        created_at
                    ) = item

                    score = calculate_match(
                        detected_objects,
                        found_type,
                        location,
                        found_location,
                        description,
                        found_description
                    )

                    matches.append(
                        (
                            score,
                            item
                        )
                    )

                # Highest score first
                matches.sort(
                    reverse=True,
                    key=lambda x: x[0]
                )

                # -----------------------------
                # DISPLAY MATCHES
                # -----------------------------

                for score, item in matches[:5]:

                    (
                        item_id,
                        found_type,
                        found_description,
                        found_location,
                        status,
                        image_path,
                        contact,
                        created_at
                    ) = item

                    if score >= 40:

                        st.markdown(
                            f"### 🎯 Match Score: {score}%"
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            if os.path.exists(
                                image_path
                            ):

                                st.image(
                                    image_path,
                                    width=250
                                )

                        with col2:

                            st.write(
                                f"**Item:** {found_type}"
                            )

                            st.write(
                                f"📍 **Location:** "
                                f"{found_location}"
                            )

                            st.write(
                                f"📝 **Description:** "
                                f"{found_description}"
                            )

                            st.write(
                                f"📞 **Contact:** "
                                f"{contact}"
                            )

                            if score >= 80:

                                st.success(
                                    "🔥 High Match!"
                                )

                            elif score >= 60:

                                st.warning(
                                    "🟡 Possible Match"
                                )

                            else:

                                st.info(
                                    "🔵 Low Match"
                                )

                        st.divider()


# ==========================================
# ALL ITEMS
# ==========================================

elif page == "📋 All Items":

    st.header("📋 All Reported Items")

    items = get_items()

    if not items:

        st.info(
            "No items reported yet."
        )

    else:

        for item in items:

            (
                item_id,
                item_type,
                description,
                location,
                status,
                image_path,
                contact,
                created_at
            ) = item

            if status == "LOST":

                st.error(
                    f"🔴 LOST — {item_type}"
                )

            else:

                st.success(
                    f"🟢 FOUND — {item_type}"
                )

            col1, col2 = st.columns(2)

            with col1:

                if os.path.exists(
                    image_path
                ):

                    st.image(
                        image_path,
                        width=250
                    )

            with col2:

                st.write(
                    f"📍 Location: {location}"
                )

                st.write(
                    f"📝 {description}"
                )

                st.write(
                    f"📅 {created_at}"
                )

            st.divider()