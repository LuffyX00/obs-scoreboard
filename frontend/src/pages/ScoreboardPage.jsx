import Scoreboard from "../components/Scoreboard";
import { useScoreboard } from "../hooks/useScoreboard";
import "../styles/scoreboard.css";

export default function ScoreboardPage() {
  const { state } = useScoreboard();

  return (
    <div className="obs-page">
      <Scoreboard state={state} />
    </div>
  );
}
