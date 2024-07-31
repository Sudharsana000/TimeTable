import React, { useState } from 'react';
import axios from 'axios';

const Timetable = () => {
    const [year1Class1Timetable, setYear1Class1Timetable] = useState({});
    const [year1Class2Timetable, setYear1Class2Timetable] = useState({});
    const [error, setError] = useState(null);

    const generateTimetable = async () => {
        try {
            const response = await axios.post('/generate');
            if (response.data) {
                setYear1Class1Timetable(response.data.class1);
                setYear1Class2Timetable(response.data.class2);
                setError(null);
            } else {
                setError('Empty response from server.');
            }
        } catch (err) {
            console.error('Error generating timetable:', err);
            setError('Failed to generate timetable. Please try again.');
        }
    };

    const renderTimetable = (timetable, title) => (
        <div className="timetable">
            <h2>{title}</h2>
            {Object.entries(timetable).map(([day, hours]) => (
                <div key={day} className="day">
                    <h3>{day}</h3>
                    {hours.map((hour, index) => (
                        <div key={index} className="hour">
                            {hour.subject ? `${hour.subject} (${hour.classroom} - ${hour.faculty})` : "Free Hour"}
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );

    return (
        <div>
            <h1>Automatic Timetable Scheduler</h1>
            <button onClick={generateTimetable}>Generate Timetable</button>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <div id="timetables">
                {renderTimetable(year1Class1Timetable, "Year 1 - Class 1 Timetable")}
                {renderTimetable(year1Class2Timetable, "Year 1 - Class 2 Timetable")}
            </div>
        </div>
    );
};

export default Timetable;

