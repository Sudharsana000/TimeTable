import React, { useState } from 'react';
import axios from 'axios';

const Timetable = () => {
    const [timetables, setTimetables] = useState([]);
    const [error, setError] = useState(null);

    const generateTimetable = async () => {
        try {
            const response = await axios.post('/generate');
            if (response.data) {
                setTimetables(response.data);
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
        <div className="timetable" key={title}>
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
                {Object.entries(timetables).map(([className, timetable]) => 
                    renderTimetable(timetable, className)
                )}
            </div>
        </div>
    );
};

export default Timetable;
