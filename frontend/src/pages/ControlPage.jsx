import { useState } from "react";
import { Link } from "react-router-dom";
import TeamSelector from "../components/TeamSelector";
import { formatTime, useScoreboard } from "../hooks/useScoreboard";
import "../styles/control.css";

const PERIODS = ["1ST HALF", "2ND HALF", "EXTRA TIME", "PENALTIES", "FULL TIME"];

export default function ControlPage() {
  const { state, teams, connected, updateState, selectTeam, setCustomTeam, setMatchType, resetState } =
    useScoreboard();
  const [busy, setBusy] = useState(false);

  const run = async (fn) => {
    setBusy(true);
    try {
      await fn();
    } finally {
      setBusy(false);
    }
  };

  const adjustScore = (team, delta) =>
    run(() =>
      updateState({
        [team]: { score: Math.max(0, state[team].score + delta) },
      })
    );

  const setTime = (minutes, seconds) =>
    run(() => updateState({ minutes, seconds }));

  return (
    <div className="control-page">
      <header className="control-header">
        <div>
          <h1>Scoreboard Control</h1>
          <p className={`status ${connected ? "status--online" : "status--offline"}`}>
            {connected ? "Connected to server" : "Reconnecting..."}
          </p>
        </div>
        <Link to="/" className="preview-link" target="_blank">
          Open OBS Overlay
        </Link>
      </header>

      <section className="control-card">
        <h2>Match Type</h2>
        <div className="match-type-buttons">
          <button
            type="button"
            disabled={busy}
            className={state.match_type === "international" ? "active" : ""}
            onClick={() => run(() => setMatchType("international"))}
          >
            International (Countries)
          </button>
          <button
            type="button"
            disabled={busy}
            className={state.match_type === "club" ? "active" : ""}
            onClick={() => run(() => setMatchType("club"))}
          >
            Club Match
          </button>
        </div>
      </section>

      <section className="control-card">
        <h2>Match</h2>
        <label>
          Tournament
          <input
            value={state.tournament}
            onChange={(e) => updateState({ tournament: e.target.value })}
          />
        </label>
        <label>
          Period
          <select
            value={state.period}
            onChange={(e) => updateState({ period: e.target.value })}
          >
            {PERIODS.map((period) => (
              <option key={period} value={period}>
                {period}
              </option>
            ))}
          </select>
        </label>
        <label className="checkbox-row">
          <input
            type="checkbox"
            checked={state.is_live}
            onChange={(e) => updateState({ is_live: e.target.checked })}
          />
          Show LIVE badge
        </label>
      </section>

      <div className="teams-grid">
        <TeamSelector
          side="home"
          team={state.home_team}
          teams={teams}
          disabled={busy}
          onSelect={(teamId) => run(() => selectTeam("home", teamId))}
          onCustomApply={(teamData) => run(() => setCustomTeam("home", teamData))}
        />
        <TeamSelector
          side="away"
          team={state.away_team}
          teams={teams}
          disabled={busy}
          onSelect={(teamId) => run(() => selectTeam("away", teamId))}
          onCustomApply={(teamData) => run(() => setCustomTeam("away", teamData))}
        />
      </div>

      <div className="teams-grid">
        <section className="control-card">
          <h2>{state.home_team.name} Score</h2>
          <div className="score-controls">
            <button disabled={busy} onClick={() => adjustScore("home_team", -1)}>
              −
            </button>
            <span className="score-display">{state.home_team.score}</span>
            <button disabled={busy} onClick={() => adjustScore("home_team", 1)}>
              +
            </button>
          </div>
        </section>

        <section className="control-card">
          <h2>{state.away_team.name} Score</h2>
          <div className="score-controls">
            <button disabled={busy} onClick={() => adjustScore("away_team", -1)}>
              −
            </button>
            <span className="score-display">{state.away_team.score}</span>
            <button disabled={busy} onClick={() => adjustScore("away_team", 1)}>
              +
            </button>
          </div>
        </section>
      </div>

      <section className="control-card">
        <h2>
          Timer — {formatTime(state.minutes, state.seconds)}
          {state.added_time > 0 ? ` (+${state.added_time})` : ""}
        </h2>
        <div className="timer-controls">
          <button
            disabled={busy}
            className={state.timer_running ? "active" : ""}
            onClick={() => updateState({ timer_running: !state.timer_running })}
          >
            {state.timer_running ? "Pause" : "Start"}
          </button>
          <button
            disabled={busy}
            onClick={() =>
              updateState({ timer_running: false, minutes: 0, seconds: 0, added_time: 0 })
            }
          >
            Reset to 00:00
          </button>
        </div>
        <div className="time-inputs">
          <label>
            Minutes
            <input
              type="number"
              min="0"
              max="120"
              value={state.minutes}
              onChange={(e) => setTime(Number(e.target.value), state.seconds)}
            />
          </label>
          <label>
            Seconds
            <input
              type="number"
              min="0"
              max="59"
              value={state.seconds}
              onChange={(e) => setTime(state.minutes, Number(e.target.value))}
            />
          </label>
        </div>
        <div className="added-time-controls">
          <label>
            Added time (minutes)
            <div className="added-time-row">
              <button
                type="button"
                disabled={busy}
                onClick={() =>
                  updateState({ added_time: Math.max(0, (state.added_time || 0) - 1) })
                }
              >
                −
              </button>
              <input
                type="number"
                min="0"
                max="20"
                value={state.added_time || 0}
                onChange={(e) =>
                  updateState({ added_time: Math.max(0, Math.min(20, Number(e.target.value))) })
                }
              />
              <button
                type="button"
                disabled={busy}
                onClick={() =>
                  updateState({ added_time: Math.min(20, (state.added_time || 0) + 1) })
                }
              >
                +
              </button>
              <button
                type="button"
                disabled={busy}
                className="added-time-clear"
                onClick={() => updateState({ added_time: 0 })}
              >
                Clear
              </button>
            </div>
          </label>
          <p className="added-time-hint">
            Shows as <strong>+3</strong> next to the clock on the overlay (set to 0 to hide).
          </p>
        </div>
      </section>

      <section className="control-card">
        <h2>Quick Presets</h2>
        <div className="preset-buttons">
          <button
            disabled={busy}
            onClick={() =>
              updateState({
                period: "1ST HALF",
                minutes: 0,
                seconds: 0,
                timer_running: false,
              })
            }
          >
            Kick Off (1st Half)
          </button>
          <button
            disabled={busy}
            onClick={() =>
              updateState({
                period: "2ND HALF",
                minutes: 45,
                seconds: 0,
                timer_running: false,
              })
            }
          >
            2nd Half Start
          </button>
          <button
            disabled={busy}
            onClick={() =>
              updateState({ period: "FULL TIME", timer_running: false })
            }
          >
            Full Time
          </button>
          <button disabled={busy} className="danger" onClick={() => resetState()}>
            Reset Everything
          </button>
        </div>
      </section>
    </div>
  );
}
