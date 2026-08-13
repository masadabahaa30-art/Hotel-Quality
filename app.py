import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام جودة الفندق",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص لتحسين المظهر والخطوط العربية
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

    * {
        font-family: 'Cairo', sans-serif;
    }

    .main {
        background-color: #f8f9fa;
    }

    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: white;
    }

    h1 {
        color: #2c3e50;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }

    h2 {
        color: #34495e;
        border-right: 5px solid #667eea;
        padding-right: 15px;
        margin-top: 30px;
    }

    .stProgress > div > div > div > div {
        background-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.title("🏨 لوحة تحكم نظام الجودة الفندقية")

# الشريط الجانبي
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0;'>🏨</h1>
    
    <h3 style='color: white; margin: 0;'>فندق البهاء/h3>
    </div>
    """, unsafe_allow_html=True)

    st.header("⚙️ الإعدادات")

    # اختيار الفترة الزمنية
    date_range = st.date_input(
        "📅 اختر الفترة الزمنية",
        value=(datetime.now() - timedelta(days=30), datetime.now())
    )

    # اختيار القسم
    department = st.selectbox(
        "🏢 اختر القسم",
        ["الكل", "الاستقبال", "الغرف", "المطعم", "المرافق", "الصيانة"]
    )

    # نوع التقرير
    report_type = st.radio(
        "📊 نوع التقرير",
        ["يومي", "أسبوعي", "شهري"]
    )

    st.markdown("---")

    if st.button("🔄 تحديث البيانات", use_container_width=True):
        st.success("تم تحديث البيانات بنجاح!")

    if st.button("📥 تحميل التقرير", use_container_width=True):
        st.info("جاري تحميل التقرير...")

    st.markdown("---")
    st.info("📅 آخر تحديث\n\n" + datetime.now().strftime("%Y-%m-%d\n%H:%M"))

# إنشاء بيانات تجريبية (يمكن استبدالها بقاعدة بيانات حقيقية)
@st.cache_data
def create_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')

    data = {
        'التاريخ': dates,
        'معدل_الرضا': np.random.uniform(4.0, 5.0, len(dates)),
        'عدد_النزلاء': np.random.randint(80, 150, len(dates)),
        'الشكاوى': np.random.randint(0, 8, len(dates)),
        'معدل_الإشغال': np.random.uniform(70, 95, len(dates))
    }

    return pd.DataFrame(data)

df = create_sample_data()

# القسم الأول: المؤشرات الرئيسية (KPIs)
st.header("📊 المؤشرات الرئيسية (KPIs)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="⭐ معدل التقييم العام",
        value="4.5/5",
        delta="+0.2"
    )

with col2:
    st.metric(
        label="😊 نسبة الرضا",
        value="89%",
        delta="+3%"
    )

with col3:
    st.metric(
        label="📝 الشكاوى الشهرية",
        value="35",
        delta="-5",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="🏨 معدل الإشغال",
        value="85%",
        delta="+7%"
    )

st.markdown("---")

# القسم الثاني: تقييم الخدمات
st.header("🎯 تقييم جودة الخدمات")

col1, col2 = st.columns([1, 1])

with col1:
    departments_data = {
        'القسم': ['🛎️ الاستقبال', '🛏️ نظافة الغرف', '🍽️ المطعم', '🏊 المرافق', '📞 خدمة العملاء'],
        'التقييم': [4.6, 4.7, 4.2, 4.4, 4.5],
        'الهدف': [4.5, 4.5, 4.5, 4.5, 4.5]
    }

    df_departments = pd.DataFrame(departments_data)

    def get_status(rating, target):
        if rating >= target + 0.1:
            return "🟢 ممتاز"
        elif rating >= target:
            return "🟡 جيد"
        else:
            return "🔴 يحتاج تحسين"

    df_departments['الحالة'] = df_departments.apply(
        lambda x: get_status(x['التقييم'], x['الهدف']), axis=1
    )

    st.dataframe(
        df_departments.style.background_gradient(subset=['التقييم'], cmap='RdYlGn'),
        use_container_width=True,
        hide_index=True
    )

with col2:
    fig_ratings = go.Figure()

    fig_ratings.add_trace(go.Bar(
        x=departments_data['القسم'],
        y=departments_data['التقييم'],
        name='التقييم الفعلي',
        marker_color='#667eea',
        text=departments_data['التقييم'],
        textposition='auto',
    ))

    fig_ratings.add_trace(go.Scatter(
        x=departments_data['القسم'],
        y=departments_data['الهدف'],
        name='الهدف المطلوب',
        mode='lines+markers',
        line=dict(color='#e74c3c', width=3, dash='dash'),
        marker=dict(size=10)
    ))

    fig_ratings.update_layout(
        title="مقارنة التقييمات بالأهداف",
        yaxis_title="التقييم (من 5)",
        yaxis=dict(range=[0, 5]),
        height=400,
        hovermode='x unified'
    )

    st.plotly_chart(fig_ratings, use_container_width=True)

st.markdown("---")

# القسم الثالث: تحليل الشكاوى
st.header("📋 تحليل الشكاوى")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    complaints_data = pd.DataFrame({
        'النوع': ['🌡️ التكييف', '🍳 الإفطار', '📶 الإنترنت', '🔇 الضوضاء', '📝 أخرى'],
        'العدد': [8, 6, 5, 4, 12]
    })

    fig_complaints = px.pie(
        complaints_data,
        values='العدد',
        names='النوع',
        title='توزيع الشكاوى حسب النوع',
        color_discrete_sequence=px.colors.sequential.Purples_r,
        hole=0.4
    )

    fig_complaints.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig_complaints, use_container_width=True)

with col2:
    st.markdown("### 📊 إحصائيات الشكاوى")

    st.metric("إجمالي الشكاوى", "35", "-5")
    st.metric("الشكاوى المحلولة", "32", "+3")
    st.metric("الشكاوى المعلقة", "3", "-2", delta_color="inverse")

    st.progress(91)
    st.caption("✅ نسبة حل الشكاوى: 91%")

with col3:
    st.markdown("### ⏱️ أوقات الاستجابة")

    response_data = pd.DataFrame({
        'الفترة': ['< ساعة', '1-2 ساعة', '2-4 ساعات', '> 4 ساعات'],
        'العدد': [15, 12, 5, 3]
    })

    fig_response = px.bar(
        response_data,
        x='الفترة',
        y='العدد',
        title='توزيع أوقات حل الشكاوى',
        color='العدد',
        color_continuous_scale='Viridis'
    )

    fig_response.update_layout(height=300)
    st.plotly_chart(fig_response, use_container_width=True)

st.markdown("---")

# القسم الرابع: معايير النظافة والصيانة
st.header("🧹 معايير النظافة والصيانة")

col1, col2, col3, col4 = st.columns(4)

standards = [
    ("🧹 نظافة الغرف", 98, "+2%"),
    ("🔧 الصيانة الدورية", 95, "+1%"),
    ("🧴 مستلزمات النظافة", 100, "0%"),
    ("🛠️ الصيانة العاجلة", 88, "-3%")
]

for idx, (col, (label, value, delta)) in enumerate(zip([col1, col2, col3, col4], standards)):
    with col:
        st.metric(label, f"{value}%", delta)
        st.progress(value)

st.markdown("---")

# القسم الخامس: أداء الموظفين
st.header("👥 تقييم أداء الموظفين")

performance_data = pd.DataFrame({
    'المعيار': ['⏰ الالتزام بالمواعيد', '🤝 اللباقة مع النزلاء', '⚡ سرعة الاستجابة', '💼 الكفاءة المهنية', '📚 التدريب المستمر'],
    'النسبة': [96, 93, 91, 94, 85]
})

fig_performance = px.bar(
    performance_data,
    x='المعيار',
    y='النسبة',
    title='تقييم أداء الموظفين (%)',
    color='النسبة',
    color_continuous_scale='Blues',
    text='النسبة'
)

fig_performance.update_traces(texttemplate='%{text}%', textposition='outside')
fig_performance.update_layout(
    height=450,
    yaxis=dict(range=[0, 110])
)

st.plotly_chart(fig_performance, use_container_width=True)

st.markdown("---")

# القسم السادس: السلامة والأمان
st.header("🔒 معايير السلامة والأمان")

col1, col2, col3 = st.columns(3)

safety_items = [
    ["✅ أنظمة الإطفاء: فحص شهري", "✅ مخارج الطوارئ: جاهزة 100%"],
    ["✅ كاميرات المراقبة: تعمل بكفاءة", "✅ الإسعافات الأولية: متوفرة"],
    ["✅ أنظمة الأمان: محدثة", "✅ تدريبات الطوارئ: منتظمة"]
]

for col, items in zip([col1, col2, col3], safety_items):
    with col:
        for item in items:
            st.success(item)

st.markdown("---")

# القسم السابع: جودة الطعام والمشروبات
st.header("🍽️ جودة الطعام والمشروبات")

col1, col2 = st.columns(2)

with col1:
    food_quality = {
        'المعيار': ['جودة الطعام', 'سرعة التقديم', 'مهارة الطهاة', 'سلامة الغذاء', 'تنوع القائمة'],
        'التقييم': [4.3, 4.1, 4.5, 5.0, 4.2]
    }

    fig_food = go.Figure(data=go.Scatterpolar(
        r=food_quality['التقييم'],
        theta=food_quality['المعيار'],
        fill='toself',
        marker=dict(color='#667eea', size=10),
        line=dict(color='#667eea', width=2)
    ))

    fig_food.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickfont=dict(size=12)
            )
        ),
        title="رادار تقييم جودة الطعام والمشروبات",
        height=450
    )

    st.plotly_chart(fig_food, use_container_width=True)

with col2:
    trend_data = pd.DataFrame({
        'الشهر': ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو'],
        'المطعم الرئيسي': [4.1, 4.2, 4.3, 4.2, 4.3],
        'مطعم البوفيه': [3.9, 4.0, 4.1, 4.2, 4.2],
        'خدمة الغرف': [4.3, 4.4, 4.3, 4.5, 4.4]
    })

    fig_trend = px.line(
        trend_data,
        x='الشهر',
        y=['المطعم الرئيسي', 'مطعم البوفيه', 'خدمة الغرف'],
        markers=True,
        title='اتجاه تقييمات خدمات الطعام'
    )

    fig_trend.update_layout(
        yaxis_title="التقييم",
        legend_title="الخدمة",
        height=450
    )

    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# القسم الثامن: التحليلات والتوصيات
st.header("💡 التحليلات والتوصيات")

col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ نقاط القوة")
    strengths = [
        "معدل رضا مرتفع (89%)",
        "نظافة ممتازة (98%)",
        "حل سريع للشكاوى (91%)",
        "أداء ممتاز للموظفين",
        "معايير سلامة متقدمة"
    ]
    for strength in strengths:
        st.success(f"✔️ {strength}")

with col2:
    st.subheader("⚠️ نقاط التحسين")
    improvements = [
        "تحسين جودة المطعم (4.2/5)",
        "تسريع خدمة الإنترنت",
        "معالجة مشاكل التكييف (8 شكاوى)",
        "تقليل وقت تقديم الإفطار",
        "زيادة التدريب (85%)"
    ]
    for improvement in improvements:
        st.warning(f"⚡ {improvement}")

st.markdown("---")

# القسم التاسع: خطة العمل
st.header("📋 خطة العمل والمتابعة")

tasks_data = pd.DataFrame({
    'المهمة': [
        '🍽️ تدريب إضافي لطاقم المطعم',
        '🌡️ صيانة شاملة لأنظمة التكييف',
        '📶 ترقية البنية التحتية للإنترنت',
        '📊 مراجعة شهرية للأداء',
        '📚 برنامج تدريب متقدم للموظفين'
    ],
    'المسؤول': ['مدير المطعم', 'مدير الصيانة', 'مدير تقنية المعلومات', 'مدير الجودة', 'مدير الموارد البشرية'],
    'الموعد النهائي': ['2024-02-15', '2024-02-10', '2024-02-20', '2024-02-28', '2024-03-01'],
    'الأولوية': ['عالية', 'عالية', 'متوسطة', 'منخفضة', 'متوسطة'],
    'الحالة': ['🟡 قيد التنفيذ', '🔴 لم تبدأ', '🟡 قيد التنفيذ', '🟢 مستمرة', '🔴 لم تبدأ']
})

def color_priority(val):
    if val == 'عالية':
        return 'background-color: #ffcccc'
    elif val == 'متوسطة':
        return 'background-color: #fff4cc'
    else:
        return 'background-color: #ccffcc'

st.dataframe(
    tasks_data.style.applymap(color_priority, subset=['الأولوية']),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# الأهداف الشهرية
st.subheader("🎯 الأهداف الشهرية")

col1, col2, col3, col4 = st.columns(4)

goals = [
    ("رفع التقييم العام إلى 4.7/5", False),
    ("تقليل الشكاوى بنسبة 20%", False),
    ("تحقيق 95% رضا في المطعم", False),
    ("صيانة 100% للغرف", True)
]

for col, (goal, status) in zip([col1, col2, col3, col4], goals):
    with col:
        st.checkbox(goal, value=status)

st.markdown("---")

# إحصائيات متقدمة (تبويبات)
st.header("📈 إحصائيات متقدمة")

tab1, tab2, tab3 = st.tabs(["📊 الاتجاهات", "💰 الإيرادات", "🌍 التوزيع الجغرافي"])

with tab1:
    fig_trends = px.line(
        df,
        x='التاريخ',
        y=['معدل_الرضا', 'معدل_الإشغال'],
        title='اتجاهات معدل الرضا والإشغال'
    )
    st.plotly_chart(fig_trends, use_container_width=True)

with tab2:
    revenue_data = pd.DataFrame({
        'الخدمة': ['الغرف', 'المطعم', 'المرافق', 'خدمات إضافية'],
        'الإيراد': [450000, 120000, 80000, 50000]
    })

    fig_revenue = px.bar(
        revenue_data,
        x='الخدمة',
        y='الإيراد',
        title='توزيع الإيرادات حسب الخدمة',
        color='الإيراد',
        color_continuous_scale='Teal'
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

with tab3:
    nationality_data = pd.DataFrame({
        'الدولة': ['السعودية', 'الإمارات', 'الكويت', 'مصر', 'الأردن', 'أخرى'],
        'العدد': [150, 80, 60, 45, 35, 30]
    })

    fig_nationality = px.pie(
        nationality_data,
        values='العدد',
        names='الدولة',
        title='توزيع النزلاء حسب الجنسية'
    )
    st.plotly_chart(fig_nationality, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 10px;'>
        <p style='color: gray; margin: 0;'>Hotel Quality Management Dashboard</p>
        <p style='color: #667eea; font-weight: bold; margin: 5px 0 0 0;'>Dr. Maiada Bahaa</p>
    </div>
    """,
    unsafe_allow_html=True
)