import { useEffect, useState } from "react";
import { TeamEmblem } from "./Scoreboard";

const EMPTY_CUSTOM = {
  type: "country",
  name: "",
  code: "",
  flag_url: "",
  primary_color: "#1a1a2e",
  secondary_color: "#c9a227",
};

export default function TeamSelector({
  side,
  team,
  teams,
  onSelect,
  onCustomApply,
  disabled,
}) {
  const [filter, setFilter] = useState("");
  const [tab, setTab] = useState(
    team.id === "custom" ? "custom" : team.type === "club" ? "club" : "country"
  );
  const [custom, setCustom] = useState(EMPTY_CUSTOM);

  useEffect(() => {
    if (team.id === "custom") {
      setTab("custom");
      setCustom({
        type: team.type,
        name: team.name,
        code: team.code,
        flag_url: team.flag_url || "",
        primary_color: team.primary_color || "#1a1a2e",
        secondary_color: team.secondary_color || "#c9a227",
      });
    } else {
      setTab(team.type === "club" ? "club" : "country");
    }
  }, [team]);

  const filtered = teams
    .filter((entry) => entry.type === tab)
    .filter((entry) => {
      const query = filter.trim().toLowerCase();
      if (!query) return true;
      return (
        entry.name.toLowerCase().includes(query) ||
        entry.code.toLowerCase().includes(query)
      );
    });

  const handleCustomChange = (field, value) => {
    setCustom((prev) => ({ ...prev, [field]: value }));
  };

  const handleCustomApply = () => {
    const name = custom.name.trim();
    const code = custom.code.trim().toUpperCase();
    if (!name || !code) return;

    onCustomApply({
      type: custom.type,
      name,
      code,
      flag_url: custom.type === "country" ? custom.flag_url.trim() || null : null,
      primary_color: custom.type === "club" ? custom.primary_color : undefined,
      secondary_color: custom.type === "club" ? custom.secondary_color : undefined,
    });
  };

  const previewTeam = {
    id: "custom",
    type: custom.type,
    name: custom.name.trim() || "Custom Team",
    code: custom.code.trim().toUpperCase() || "CUS",
    flag_url: custom.type === "country" ? custom.flag_url.trim() || null : null,
    primary_color: custom.primary_color,
    secondary_color: custom.secondary_color,
  };

  return (
    <section className="control-card team-selector">
      <div className="team-selector__header">
        <h2>{side === "home" ? "Home Team" : "Away Team"}</h2>
        <div className="team-selector__current">
          <TeamEmblem team={team} />
          <div>
            <strong>{team.name}</strong>
            <span>
              {team.code} ·{" "}
              {team.id === "custom"
                ? "Custom"
                : team.type === "club"
                  ? "Club"
                  : "Country"}
            </span>
          </div>
        </div>
      </div>

      <div className="team-tabs">
        <button
          type="button"
          className={tab === "country" ? "active" : ""}
          onClick={() => setTab("country")}
          disabled={disabled}
        >
          Countries
        </button>
        <button
          type="button"
          className={tab === "club" ? "active" : ""}
          onClick={() => setTab("club")}
          disabled={disabled}
        >
          Clubs
        </button>
        <button
          type="button"
          className={tab === "custom" ? "active" : ""}
          onClick={() => setTab("custom")}
          disabled={disabled}
        >
          Custom
        </button>
      </div>

      {tab === "custom" ? (
        <div className="custom-team-form">
          <label>
            Team name
            <input
              value={custom.name}
              onChange={(e) => handleCustomChange("name", e.target.value)}
              placeholder="e.g. Kathmandu FC"
              disabled={disabled}
            />
          </label>
          <label>
            Team code (2–4 letters)
            <input
              value={custom.code}
              onChange={(e) => handleCustomChange("code", e.target.value.toUpperCase())}
              placeholder="e.g. KTM"
              maxLength={4}
              disabled={disabled}
            />
          </label>
          <label>
            Display type
            <select
              value={custom.type}
              onChange={(e) => handleCustomChange("type", e.target.value)}
              disabled={disabled}
            >
              <option value="country">Country (flag)</option>
              <option value="club">Club (badge)</option>
            </select>
          </label>

          {custom.type === "country" ? (
            <label>
              Flag image URL (optional)
              <input
                value={custom.flag_url}
                onChange={(e) => handleCustomChange("flag_url", e.target.value)}
                placeholder="https://example.com/flag.png"
                disabled={disabled}
              />
            </label>
          ) : (
            <div className="color-inputs">
              <label>
                Primary color
                <input
                  type="color"
                  value={custom.primary_color}
                  onChange={(e) => handleCustomChange("primary_color", e.target.value)}
                  disabled={disabled}
                />
              </label>
              <label>
                Secondary color
                <input
                  type="color"
                  value={custom.secondary_color}
                  onChange={(e) => handleCustomChange("secondary_color", e.target.value)}
                  disabled={disabled}
                />
              </label>
            </div>
          )}

          <div className="custom-team-preview">
            <span>Preview</span>
            <TeamEmblem team={previewTeam} />
            <strong>{previewTeam.code}</strong>
            <small>{previewTeam.name}</small>
          </div>

          <button
            type="button"
            className="custom-team-apply"
            onClick={handleCustomApply}
            disabled={disabled || !custom.name.trim() || !custom.code.trim()}
          >
            Apply Custom Team
          </button>
        </div>
      ) : (
        <>
          <input
            className="team-search"
            placeholder={`Search ${tab === "country" ? "countries" : "clubs"}...`}
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            disabled={disabled}
          />

          <div className="team-grid">
            {filtered.map((entry) => (
              <button
                key={entry.id}
                type="button"
                className={`team-option ${entry.id === team.id ? "selected" : ""}`}
                onClick={() => onSelect(entry.id)}
                disabled={disabled}
              >
                <TeamEmblem team={entry} />
                <span className="team-option__code">{entry.code}</span>
                <span className="team-option__name">{entry.name}</span>
              </button>
            ))}
          </div>
        </>
      )}
    </section>
  );
}
