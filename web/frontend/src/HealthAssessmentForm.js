import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './style.css';

const HealthAssessmentForm = () => {

      const allFields = [
  "SRSEX",
  "SRAGE_P1",
  "MARIT",
  "OCCMAIN2",
  "RBMI",
  "AC207",
  "AC208",
  "BINGE30",
  "AC212",
  "AC81C",
  "SMOKING",
  "AF81",
  "AJ29",
  "AJ31",
  "HOUSETYPE",
  "MAREXPOSE",
  "DSTRSYR",
  "WGHTK_P",
  "AC174",
];


//    const initialState = allFields.reduce((acc, field) => {
//      acc[field] = "";
//      return acc;
//    }, {});

    const initialState = {
  "SRSEX": "1",               // Male
  "SRAGE_P1": "21.5",         // 18-25 years
  "OMBSRR_P1": "1",           // Hispanic
  "DISABILITY": "1",          // Disabled
  "MARIT": "0",               // Married
  "OCCMAIN2": "1",            // Management, business, and financial
  "UR_CLRT4": "1",            // Urban
  "RBMI": "0",                // Underweight 0-18.49
  "AC207": "1",               // Yes
  "AC208": "3",               // Never
  "BINGE30": "1",             // Yes
  "AC212": "1",               // Yes
  "AC81C": "1",               // Yes
  "SMKEXPOSE": "1",           // Yes
  "SMOKING": "1",             // Currently smokes
  "NUMCIG": "0",              // None
  "AF81": "1",                // Yes
  "AJ29": "5",                // All of the time
  "AJ31": "1",                // All of the time
  "HOUSETYPE": "1",           // Renting in multi-unit building
  "MAREXPOSE": "1",           // Yes
  "DSTRSYR": "1"              // Yes
}


  const [formData, setFormData] = useState(initialState);
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsLoading(true);
    fetch('/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error('Network response was not ok');
        }
        return res.json();
      })
      .then((data) => {
        setIsLoading(false);
        // Navigate to the result page and pass the result and formData via state
        navigate('/result', { state: { result: data, formData } });
      })
      .catch((error) => {
        setIsLoading(false);
        console.error('Error submitting form:', error);
        navigate('/result', { state: { result: `<p>Error: ${error.message}</p>` } });
      });
  };

  return (
    <div className="container">
      <div className="card">
        <h2 className="heading">🩺 Health assessment form</h2>
        <p className="description">
          Please complete the following health assessment to help us understand your current health status. Your responses will help tailor a personalized report.
        </p>
        <form onSubmit={handleSubmit}>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">1. Self-reported gender:</label>
            <select name="SRSEX" value={formData.SRSEX || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="1">Male</option>
              <option value="2">Female</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">2. Self-reported age:</label>
            <select name="SRAGE_P1" value={formData.SRAGE_P1 || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="21.5">18-25 years</option>
              <option value="27.5">26-29 years</option>
              <option value="32">30-34 years</option>
              <option value="37">35-39 years</option>
              <option value="42">40-44 years</option>
              <option value="47">45-49 years</option>
              <option value="52">50-54 years</option>
              <option value="57">55-59 years</option>
              <option value="62">60-64 years</option>
              <option value="67">65-69 years</option>
              <option value="72">70-74 years</option>
              <option value="77">75-79 years</option>
              <option value="82">80-84 years</option>
              <option value="87">85+ years</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">3. Race/Ethnicity:</label>
            <select name="OMBSRR_P1" value={formData.OMBSRR_P1 || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="1">Hispanic</option>
              <option value="2">White, Non-Hispanic</option>
              <option value="3">African American Only, Not Hispanic</option>
              <option value="4">American Indian/Alaskan Native Only, NH</option>
              <option value="5">Asian Only, NH</option>
              <option value="6">Other/Two or More Races</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">4. Disability status due to physical/mental/emotional condition:</label>
            <select name="DISABILITY" value={formData.DISABILITY || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="1">Disabled</option>
              <option value="2">Not disabled</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">5. Marital status:</label>
            <select name="MARIT" value={formData.MARIT || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="0">Married</option>
              <option value="1">Other/Sep/Div/Living with partner</option>
              <option value="2">Never married</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">6. Main occupation:</label>
            <select name="OCCMAIN2" value={formData.OCCMAIN2 || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="1">Management, business, and financial</option>
              <option value="2">Computer, engineering, and science</option>
              <option value="3">Education, legal, community service, art</option>
              <option value="4">Healthcare practitioners and technical</option>
              <option value="5">Service occupations</option>
              <option value="6">Sales and related occupations</option>
              <option value="7">Office and administrative support</option>
              <option value="8">Farming, fishing, and forestry</option>
              <option value="9">Construction and extraction</option>
              <option value="10">Installation, maintenance, and repair</option>
              <option value="11">Production occupations</option>
              <option value="12">Transportation and material moving</option>
              <option value="13">Military specific occupations</option>
              <option value="14">Occupation coded as not in labor force</option>
              <option value="15">Could not be coded</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">7. Living area:</label>
            <select name="UR_CLRT4" value={formData.UR_CLRT4 || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="1">Urban</option>
              <option value="2">Mixed</option>
              <option value="3">Suburban</option>
              <option value="4">Rural</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">8. BMI Descriptive:</label>
            <select name="RBMI" value={formData.RBMI || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="0">Underweight 0-18.49</option>
              <option value="1">Normal 18.5-24.99</option>
              <option value="2">Overweight 25.0-29.99</option>
              <option value="3">Obese 30.0+</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">9. Weight: kg:</label>
            <input type="number" name="WGHTK_P" value={formData.WGHTK_P || ''} onChange={handleChange} min="30" max="150" required className="input" />
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">10. Number of days smoked cigarettes in past 30 days:</label>
            <input type="number" name="AC174" value={formData.AC174 || ''} onChange={handleChange} min="0" max="30" required className="input" />
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">11. Ever had an alcoholic beverage:</label>
            <select name="AC207" value={formData.AC207 || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="1">Yes</option>
              <option value="2">No</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">12. How long since last drank an alcoholic beverage:</label>
            <select name="AC208" value={formData.AC208 || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="3">Never</option>
              <option value="0">Within the past 30 days</option>
              <option value="1">More than 30 days ago</option>
              <option value="2">More than 12 months ago</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">13. Binge drinking in past 30 days:</label>
            <select name="BINGE30" value={formData.BINGE30 || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="1">Yes</option>
              <option value="2">No</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">14. Did moderate physical activity for 2.5 hours in past week:</label>
            <select name="AC212" value={formData.AC212 || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="1">Yes</option>
              <option value="2">No</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">15. Ever smoked electronic cigarettes:</label>
            <select name="AC81C" value={formData.AC81C || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="1">Yes</option>
              <option value="2">No</option>
            </select>
          </div>


            <div style={{ marginBottom: '16px' }}>
              <label className="label">16. Secondhand exposure to tobacco or marijuana smoke in past month:</label>
              <select name="SMKEXPOSE" value={formData.SMKEXPOSE || ''} onChange={handleChange} required className="select">
                <option value="">Please select</option>
                <option value="1">Yes</option>
                <option value="2">No</option>
              </select>
            </div>

            <div style={{ marginBottom: '16px' }}>
              <label className="label">17. Current smoking habits:</label>
              <select name="SMOKING" value={formData.SMOKING || ''} onChange={handleChange} required className="select">
                <option value="">Please select</option>
                <option value="1">Currently smokes</option>
                <option value="2">Quit smoking</option>
                <option value="3">Never smoked regularly</option>
              </select>
            </div>


            <div style={{ marginBottom: '16px' }}>
              <label className="label">18. Number of cigarettes per day:</label>
              <select name="NUMCIG" value={formData.NUMCIG || ''} onChange={handleChange} required className="select">
                <option value="">Please select</option>
                <option value="0">None</option>
                <option value="1">&le; 1 cigarettes</option>
                <option value="2">2–5 cigarettes</option>
                <option value="3">6–10 cigarettes</option>
                <option value="4">11–19 cigarettes</option>
                <option value="5">20 or more</option>
              </select>
            </div>

            <div style={{ marginBottom: '16px' }}>
              <label className="label">19. Needed help for emotional/mental or alcohol/drug problem in past year:</label>
              <select name="AF81" value={formData.AF81 || ''} onChange={handleChange} required className="select">
                <option value="">Please select</option>
                <option value="1">Yes</option>
                <option value="2">No</option>
              </select>
            </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">20. Feel nervous past 30 days:</label>
            <select name="AJ29" value={formData.AJ29 || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="5">All of the time</option>
              <option value="4">Most of the time</option>
              <option value="3">Some of the time</option>
              <option value="2">A little of the time</option>
              <option value="1">Not at all</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label className="label">21. Feel restless past 30 days:</label>
            <select name="AJ31" value={formData.AJ31 || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="1">All of the time</option>
              <option value="2">Most of the time</option>
              <option value="3">Some of the time</option>
              <option value="4">A little of the time</option>
              <option value="5">Not at all</option>
            </select>
          </div>


          <div style={{ marginBottom: '16px' }}>
            <label className="label">22. Housing status:</label>
            <select name="HOUSETYPE" value={formData.HOUSETYPE || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="1">Renting in multi-unit building</option>
              <option value="2">Renting in single-unit building</option>
              <option value="3">Homeowner in multi-unit building</option>
              <option value="4">Homeowner in single-unit building</option>
              <option value="5">Living with other arrangements</option>
            </select>
          </div>


          <div style={{ marginBottom: '16px' }}>
            <label className="label">23. Exposed to marijuana smoke in past year:</label>
            <select name="MAREXPOSE" value={formData.MAREXPOSE || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="1">Yes</option>
              <option value="2">No</option>
            </select>
          </div>


          <div style={{ marginBottom: '16px' }}>
            <label className="label">24. Likely has had psychological distress in the last year:</label>
            <select name="DSTRSYR" value={formData.DSTRSYR || ''} onChange={handleChange} required className="select">
              <option value="">Please select</option>
              <option value="1">Yes</option>
              <option value="2">No</option>
            </select>
          </div>


          <button
              type="submit"
              className="button"
              disabled={isLoading}
          >
            {isLoading ? (
                <>
                  <span className="mr-2">Submitting...</span>
                  <span className="inline-block animate-spin">⚙️</span>
                </>
            ) : (
                'Submit assessment'
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default HealthAssessmentForm;



