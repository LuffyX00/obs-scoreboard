import { useEffect, useRef, useState } from "react";

const DEFAULT_STATE = {
  match_type: "international",
  tournament: "FIFA WORLD CUP 2026",
  home_team: {
    id: "arg",
    type: "country",
    name: "Argentina",
    code: "ARG",
    score: 0,
    flag_url: "https://flagcdn.com/w80/ar.png",
  },
  away_team: {
    id: "esp",
    type: "country",
    name: "Spain",
    code: "SPA",
    score: 0,
    flag_url: "https://flagcdn.com/w80/es.png",
  },
  minutes: 0,
  seconds: 0,
  period: "1ST HALF",
  added_time: 0,
  is_live: true,
  timer_running: false,
};

function getWsUrl() {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const host = import.meta.env.DEV ? "localhost:8000" : window.location.host;
  return `${protocol}//${host}/ws`;
}

export function useScoreboard() {
  const [state, setState] = useState(DEFAULT_STATE);
  const [teams, setTeams] = useState([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(null);
  const reconnectRef = useRef(null);

  useEffect(() => {
    let cancelled = false;

    const connect = () => {
      const ws = new WebSocket(getWsUrl());
      wsRef.current = ws;

      ws.onopen = () => {
        if (!cancelled) setConnected(true);
      };

      ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.type === "state") {
          setState(message.data);
        }
      };

      ws.onclose = () => {
        setConnected(false);
        if (!cancelled) {
          reconnectRef.current = window.setTimeout(connect, 1500);
        }
      };

      ws.onerror = () => ws.close();
    };

    fetch("/api/state")
      .then((res) => res.json())
      .then((data) => setState(data))
      .catch(() => {});

    fetch("/api/teams")
      .then((res) => res.json())
      .then((data) => setTeams(data))
      .catch(() => {});

    connect();

    return () => {
      cancelled = true;
      if (reconnectRef.current) clearTimeout(reconnectRef.current);
      wsRef.current?.close();
    };
  }, []);

  const updateState = async (payload) => {
    const res = await fetch("/api/state", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    setState(data);
    return data;
  };

  const selectTeam = async (side, teamId) => {
    const res = await fetch("/api/teams/select", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ side, team_id: teamId }),
    });
    const data = await res.json();
    setState(data);
    return data;
  };

  const setCustomTeam = async (side, teamData) => {
    const res = await fetch("/api/teams/custom", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ side, ...teamData }),
    });
    const data = await res.json();
    setState(data);
    return data;
  };

  const setMatchType = async (matchType) => {
    const res = await fetch("/api/match-type", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ match_type: matchType }),
    });
    const data = await res.json();
    setState(data);
    return data;
  };

  const resetState = async () => {
    const res = await fetch("/api/reset", { method: "POST" });
    const data = await res.json();
    setState(data);
    return data;
  };

  return {
    state,
    teams,
    connected,
    updateState,
    selectTeam,
    setCustomTeam,
    setMatchType,
    resetState,
  };
}

export function formatTime(minutes, seconds) {
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}
