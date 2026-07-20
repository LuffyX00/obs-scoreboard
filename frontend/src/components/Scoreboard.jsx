import wctrophy from "../trophy/wctrophy.png"

export function TeamEmblem({ team }) {
  if (team.type === "country" && team.flag_url) {
    return (
      <img
        src={team.flag_url}
        alt={`${team.name} flag`}
        className="flag flag--country"
      />
    );
  }

  return (
    <div
      className="club-badge"
      style={{
        background: `linear-gradient(135deg, ${team.primary_color || "#1a1a2e"} 0%, ${team.secondary_color || "#c9a227"} 100%)`,
      }}
      aria-label={`${team.name} badge`}
    >
      <span className="club-badge__text">{team.code}</span>
    </div>
  );
}

function TrophyIcon() {
  return (
       <img  className="trophy-icon" src={wctrophy} alt="trophy-image" />
  );
}

// function BrandLogo() {
//   return (
//     <div className="brand-logo">
//       <span className="brand-logo__ag7">AG7</span>
//       <span className="brand-logo__vloss">VLOSS</span>
//     </div>
//   );
// }

export default function Scoreboard({ state }) {
  const {
    home_team,
    away_team,
    minutes,
    seconds,
    period,
    tournament,
    is_live,
    added_time = 0,
  } = state;
  const time = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

  return (
    <div className="scoreboard-stage">
      {/* <BrandLogo /> */}

      <div className="scoreboard">
        {is_live && <div className="live-badge">LIVE</div>}

        <div className="tournament-banner">
          <span>{tournament}</span>
        </div>

        <div className="main-bar">
          <div className="team-block team-block--home">
            <TeamEmblem team={home_team} />
            <div className="team-labels">
              <span className="team-code">{home_team.code}</span>
              <span className="team-name">{home_team.name}</span>
            </div>
            <span className="team-score">{home_team.score}</span>
          </div>

          <div className="score-center">
            <span className="score-dash">-</span>
            <TrophyIcon />
            <span className="score-dash">-</span>
          </div>

          <div className="team-block team-block--away">
            <span className="team-score">{away_team.score}</span>
            <div className="team-labels team-labels--away">
              <span className="team-code">{away_team.code}</span>
              <span className="team-name">{away_team.name}</span>
            </div>
            <TeamEmblem team={away_team} />
          </div>
        </div>

        <div className="timer-panel">
          <div className="timer-panel__time">
            <span>{time}</span>
            {added_time > 0 && (
              <span className="timer-panel__added">+{added_time}</span>
            )}
          </div>
          <div className="timer-panel__period">{period}</div>
        </div>
      </div>

      {/* <div className="floor-glow" /> */}
    </div>
  );
}
