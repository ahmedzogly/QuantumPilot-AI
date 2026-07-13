import { createContext, useState, useContext } from 'react'

const translations = {
  en: {
    title: "QuantumPilot AI",
    subtitle: "AI Orchestration Platform for Quantum Computing",
    copilot_title: "Quantum Copilot",
    copilot_subtitle: "Natural language intent to execution plan",
    copilot_placeholder: "e.g., Execute with lowest cost or Choose high fidelity backend",
    build_plan: "Build Plan",
    space_weather: "Live Space Weather",
    space_weather_sub: "Real-time environmental factors affecting qubit coherence",
    backends: "Quantum Backends",
    backends_sub: "Live calibration from IBM Quantum - 156 qubit Heron R2 processors",
    training: "Decision Engine Training",
    training_sub: "NeuralUCB contextual bandit - 8847 real contexts",
    drift: "Qubit Drift Analysis",
    drift_sub: "T1 relaxation time variation from 8.04M calibration records",
    kp_correlation: "Environmental Correlation",
    kp_correlation_sub: "Novel analysis: Geomagnetic activity impact on decoherence",
    mitigation: "Error Mitigation",
    mitigation_sub: "Adaptive strategy selection with overhead optimization",
    dataset_lineage: "Data Lineage",
    live_data: "Live Data",
    backend: "Backend",
    optimization: "Optimization",
    mitigation_strategy: "Mitigation",
    shots: "Shots",
    fidelity: "Fidelity",
    cost: "Cost",
    queue: "Queue",
    explanation: "Explanation",
    risk: "Risk Level",
    neutron_flux: "Neutron Flux",
    solar_zenith: "Solar Zenith",
    temperature: "Temperature",
    cosmic_ray: "Cosmic Ray Strength",
    recommendation: "Recommendation",
    status: "Status",
    operational: "Operational",
    last_update: "Last Update",
    examples: "Examples",
    intent: "Intent",
    plan: "Execution Plan",
    expected: "Expected",
    weights: "Weights",
    language: "العربية",
    ibm_quantum: "IBM Quantum",
    live: "Live",
    contexts: "Contexts",
    loss: "Loss",
    overhead: "Overhead",
    method: "Method",
    value: "Value"
  },
  ar: {
    title: "QuantumPilot AI",
    subtitle: "منصة تنسيق ذكية للحوسبة الكمومية",
    copilot_title: "المساعد الكمومي",
    copilot_subtitle: "تحويل النية الطبيعية إلى خطة تنفيذ",
    copilot_placeholder: "مثال: نفذ بأقل تكلفة أو اختر جهاز بدقة عالية",
    build_plan: "بناء الخطة",
    space_weather: "الطقس الفضائي المباشر",
    space_weather_sub: "العوامل البيئية المؤثرة على تماسك الكيوبت في الوقت الفعلي",
    backends: "المعالجات الكمومية",
    backends_sub: "معايرة حية من IBM Quantum - معالجات Heron R2 بـ 156 كيوبت",
    training: "تدريب محرك القرار",
    training_sub: "NeuralUCB contextual bandit - 8847 سياق حقيقي",
    drift: "تحليل انجراف الكيوبت",
    drift_sub: "تغير زمن الاسترخاء T1 من 8.04 مليون سجل معايرة",
    kp_correlation: "الارتباط البيئي",
    kp_correlation_sub: "تحليل جديد: تأثير النشاط الجيومغناطيسي على تلاشي التماسك",
    mitigation: "تخفيف الأخطاء",
    mitigation_sub: "اختيار استراتيجية تكيفية مع تحسين التكلفة",
    dataset_lineage: "مصدر البيانات",
    live_data: "بيانات حية",
    backend: "المعالج",
    optimization: "التحسين",
    mitigation_strategy: "التخفيف",
    shots: "عدد القياسات",
    fidelity: "الدقة",
    cost: "التكلفة",
    queue: "الطابور",
    explanation: "التفسير",
    risk: "مستوى الخطر",
    neutron_flux: "تدفق النيوترونات",
    solar_zenith: "زاوية الشمس",
    temperature: "درجة الحرارة",
    cosmic_ray: "قوة الأشعة الكونية",
    recommendation: "التوصية",
    status: "الحالة",
    operational: "يعمل",
    last_update: "آخر تحديث",
    examples: "أمثلة",
    intent: "النية",
    plan: "خطة التنفيذ",
    expected: "المتوقع",
    weights: "الأوزان",
    language: "English",
    ibm_quantum: "IBM Quantum",
    live: "مباشر",
    contexts: "السياقات",
    loss: "الخسارة",
    overhead: "التكلفة الإضافية",
    method: "الطريقة",
    value: "القيمة"
  }
}

const LanguageContext = createContext()

export function LanguageProvider({ children }) {
  const [locale, setLocale] = useState('en')
  const t = (key) => {
    return translations[locale][key] || key
  }
  const toggleLocale = () => {
    setLocale(prev => prev === 'en' ? 'ar' : 'en')
  }
  return (
    <LanguageContext.Provider value={{ locale, t, toggleLocale, translations }}>
      <div dir={locale === 'ar' ? 'rtl' : 'ltr'} style={{ fontFamily: locale === 'ar' ? 'Tajawal, IBM Plex Sans Arabic, sans-serif' : 'IBM Plex Sans, Inter, sans-serif' }}>
        {children}
      </div>
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  return useContext(LanguageContext)
}

export default LanguageContext
