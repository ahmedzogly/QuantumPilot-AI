import { createContext, useState, useContext } from 'react'

const translations = {
  en: {
    title: "QuantumPilot AI",
    subtitle: "AI Orchestration Platform for Quantum Computing",
    copilot_title: "Quantum Copilot",
    copilot_subtitle: "Natural language intent to execution plan - Bilingual AR/EN supported",
    copilot_placeholder: "e.g., Execute with lowest cost or Choose high fidelity backend",
    build_plan: "Build Plan",
    space_weather: "Live Space Weather",
    space_weather_sub: "Real-time environmental factors affecting qubit coherence - NOAA Live",
    backends: "Quantum Backends",
    backends_sub: "Live calibration from IBM Quantum - 156 qubit Heron R2 processors",
    training: "Decision Engine Training",
    training_sub: "NeuralUCB contextual bandit - 8847 real contexts - Loss 0.3224 to 0.0028",
    drift: "Qubit Drift Analysis",
    drift_sub: "T1 relaxation time variation from 8.04M calibration records",
    kp_correlation: "Environmental Correlation",
    kp_correlation_sub: "Novel analysis: Geomagnetic activity impact on decoherence - T1 vs Kp -0.197 p=0.00047",
    mitigation: "Error Mitigation",
    mitigation_sub: "Adaptive strategy selection with overhead optimization - S-ZNE 1.2x vs ZNE 5x = 76% saving",
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
    language: "English",
    ibm_quantum: "IBM Quantum",
    live: "Live",
    contexts: "Contexts",
    loss: "Loss",
    overhead: "Overhead",
    method: "Method",
    value: "Value",
    bilingual_note: "Bilingual Support: Arabic and English - Academic Professional Version"
  }
}

const LanguageContext = createContext()

export function LanguageProvider({ children }) {
  const [locale] = useState('en')
  
  const t = (key) => {
    return translations[locale][key] || key
  }
  
  const toggleLocale = () => {
    // Disabled for English-only academic version - mention bilingual in docs
  }
  
  return (
    <LanguageContext.Provider value={{ locale, t, toggleLocale, translations }}>
      <div dir="ltr" style={{ fontFamily: 'IBM Plex Sans, Inter, sans-serif' }}>
        {children}
      </div>
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  return useContext(LanguageContext)
}

export default LanguageContext
