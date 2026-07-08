import React, { useState, useMemo, useEffect, useRef, useLayoutEffect } from 'react';
import { Clock, User, Plus, Edit2, Trash2, X, History, Zap, Download, Upload, Copy, Check, ListPlus, Link2, Users } from 'lucide-react';

// Utility for precise deterministic time calculation (ignoring complex leap year shifts for sci-fi simplicity)
// Year = 365.25 days, Month = 30.4375 days
const toMinutes = (dateStr, timeStr) => {
  if (!dateStr) return 0;
  let y = 0, m = 0, d = 0;
  const match = dateStr.match(/^(-?\d+)-(\d+)-(\d+)$/);
  if (match) {
    y = parseInt(match[1] || 0);
    m = parseInt(match[2] || 0);
    d = parseInt(match[3] || 0);
  }
  const tParts = (timeStr || "00:00").split(':');
  const hh = parseInt(tParts[0] || 0);
  const mm = parseInt(tParts[1] || 0);

  return (y * 525960) + (m * 43830) + (d * 1440) + (hh * 60) + mm;
};

const formatDisplayAge = (ageDate) => {
  const match = ageDate.match(/^(-?\d+)-(\d+)-(\d+)$/);
  if(!match) return ageDate;
  return `${parseInt(match[1])}y ${parseInt(match[2])}m ${parseInt(match[3])}d`;
};

const formatJump = (jumpMinutes) => {
  const isPast = jumpMinutes < 0;
  let mins = Math.abs(jumpMinutes);

  const years = Math.floor(mins / 525960);
  mins %= 525960;
  const months = Math.floor(mins / 43830);
  mins %= 43830;
  const days = Math.floor(mins / 1440);

  let parts = [];
  if (years > 0) parts.push(`${years}y`);
  if (months > 0) parts.push(`${months}m`);
  if (days > 0) parts.push(`${days}d`);

  if (parts.length === 0) return isPast ? "Minor backward jump" : "Minor forward jump";
  return `Jumped ${isPast ? 'back' : 'forward'} ${parts.join(' ')}`;
};

// Log-proportional vertical spacing between timeline cards: near-simultaneous
// events pack tight, two blocks 20 years apart in the same column reads as
// "normal", and each further 10x in elapsed time doubles the gap (capped so
// multi-millennia jumps don't blow out the page).
const YEAR_MINUTES = 525960;
const NORMAL_GAP_PX = 64;
const NORMAL_GAP_YEARS = 10;
const MIN_GAP_PX = 4;
const MAX_GAP_PX = NORMAL_GAP_PX * 5;

const computeGapPx = (deltaMinutes) => {
  const deltaYears = Math.max(Math.abs(deltaMinutes), 1) / YEAR_MINUTES;
  const raw = NORMAL_GAP_PX * (1 + Math.log10(deltaYears / NORMAL_GAP_YEARS));
  return Math.min(Math.max(raw, MIN_GAP_PX), MAX_GAP_PX);
};

// Shared inverse of toMinutes, for applying a delta back onto a date/time pair
// (used by the world<->age link toggle and the age +/- steppers).
const pad = (n, len = 2) => String(n).padStart(len, '0');

const minutesToDateTime = (totalMinutes) => {
  const sign = totalMinutes < 0 ? '-' : '';
  let abs = Math.round(Math.abs(totalMinutes));
  const y = Math.floor(abs / 525960); abs %= 525960;
  const m = Math.floor(abs / 43830); abs %= 43830;
  const d = Math.floor(abs / 1440); abs %= 1440;
  const hh = Math.floor(abs / 60); abs %= 60;
  const mm = abs;
  return {
    date: `${sign}${pad(y, 4)}-${pad(m)}-${pad(d)}`,
    time: `${pad(hh)}:${pad(mm)}`,
  };
};

const shiftDateTime = (dateStr, timeStr, deltaMinutes) => minutesToDateTime(toMinutes(dateStr, timeStr) + deltaMinutes);

// Timeline geometry. Cards are placed with absolute pixel positions (not CSS
// margins) because a row's flow-layout height is dictated by its own card's
// content, which decouples "gap I asked for" from "distance between dots" as
// soon as an interleaved opposite-side card has real height. Two rendering
// lanes (desktop only - mobile is a single column) each advance from their
// own previous same-lane card, so a lane's own tight/normal/double rhythm is
// preserved regardless of what the other lane is doing; a lane's very first
// entry seeds from its immediate predecessor in the merged sequence so it
// doesn't just start at the top of the page.
const DEFAULT_CARD_HEIGHT = 170;
// Every dot sits on the same central line regardless of lane, so two
// consecutive dots (in full chronological order) must never overlap - they
// may touch, hence a minimum equal to the dot's own rendered diameter.
const DOT_SIZE_PX = 16;

const computeTimelineLayout = (sortedEvents, heights, isWorld, isDesktop) => {
  const tops = [];
  const centers = [];
  const bottoms = [];
  for (let i = 0; i < sortedEvents.length; i++) {
    const h = heights[sortedEvents[i].id] || DEFAULT_CARD_HEIGHT;
    let top;
    if (i === 0) {
      top = 0;
    } else {
      const compareIdx = (!isDesktop || i === 1) ? i - 1 : i - 2;
      const a = sortedEvents[compareIdx];
      const b = sortedEvents[i];
      const aMin = isWorld ? toMinutes(a.worldDate, a.worldTime) : toMinutes(a.ageDate, a.ageTime);
      const bMin = isWorld ? toMinutes(b.worldDate, b.worldTime) : toMinutes(b.ageDate, b.ageTime);
      top = bottoms[compareIdx] + computeGapPx(bMin - aMin);
    }
    let center = top + h / 2;
    if (i > 0 && center < centers[i - 1] + DOT_SIZE_PX) {
      center = centers[i - 1] + DOT_SIZE_PX;
      top = center - h / 2;
    }
    tops.push(top);
    centers.push(center);
    bottoms.push(top + h);
  }
  const positions = {};
  sortedEvents.forEach((ev, i) => {
    positions[ev.id] = { top: tops[i], center: centers[i], height: heights[ev.id] || DEFAULT_CARD_HEIGHT };
  });
  return { positions, totalHeight: bottoms.length ? bottoms[bottoms.length - 1] : 0 };
};

// Actor color blending: each actor's event-title color blends smoothly from
// colorStart to colorEnd across that actor's own earliest-to-oldest age span.
const hexToRgb = (hex) => {
  const m = hex.replace('#', '').match(/.{1,2}/g).map(x => parseInt(x, 16));
  return { r: m[0], g: m[1], b: m[2] };
};
const rgbToHex = ({ r, g, b }) => '#' + [r, g, b].map(x => Math.round(Math.max(0, Math.min(255, x))).toString(16).padStart(2, '0')).join('');
const blendColors = (hexA, hexB, t) => {
  const a = hexToRgb(hexA), b = hexToRgb(hexB);
  return rgbToHex({ r: a.r + (b.r - a.r) * t, g: a.g + (b.g - a.g) * t, b: a.b + (b.b - a.b) * t });
};

const DEFAULT_ACTORS = [
  { id: 1, name: 'The Traveler', colorStart: '#22d3ee', colorEnd: '#c084fc' },
];

const initialEvents = [
  {
    id: 1, actorId: 1,
    title: "Birth of the Traveler",
    description: "Born in a quiet town, long before the concept of time travel was ever realized.",
    worldDate: "1990-04-12", worldTime: "08:30",
    ageDate: "0000-00-00", ageTime: "00:00"
  },
  {
    id: 2, actorId: 1,
    title: "The Accident",
    description: "A university laboratory experiment goes critically wrong, uncontrollably hurling the traveler into the future.",
    worldDate: "2026-05-14", worldTime: "15:45",
    ageDate: "0036-01-02", ageTime: "07:15"
  },
  {
    id: 3, actorId: 1,
    title: "Trapped in the Wasteland",
    description: "Arrives in a desolate future. Spends 5 long years surviving and attempting to rebuild the time engine from scrap.",
    worldDate: "2075-09-01", worldTime: "10:00",
    ageDate: "0036-01-02", ageTime: "07:16"
  },
  {
    id: 4, actorId: 1,
    title: "Return to the Past",
    description: "Successfully powers the jury-rigged machine to prevent the original accident, but dramatically overshoots the target year.",
    worldDate: "1985-10-26", worldTime: "01:20",
    ageDate: "0041-01-02", ageTime: "10:00"
  },
  {
    id: 5, actorId: 1,
    title: "Meeting the Parents",
    description: "Inadvertently encounters their own parents as teenagers, creating a dangerous paradox that must be resolved.",
    worldDate: "1988-06-15", worldTime: "12:00",
    ageDate: "0043-08-20", ageTime: "20:30"
  }
];

export default function App() {
  const [events, setEvents] = useState([...initialEvents]);
  const [actors, setActors] = useState(DEFAULT_ACTORS);
  const [selectedActorId, setSelectedActorId] = useState(DEFAULT_ACTORS[0].id);
  const [viewMode, setViewMode] = useState('world');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isIOModalOpen, setIsIOModalOpen] = useState(false);
  const [isActorModalOpen, setIsActorModalOpen] = useState(false);
  const [editingEvent, setEditingEvent] = useState(null);
  const [editingActor, setEditingActor] = useState(null);
  const [actorForm, setActorForm] = useState({ name: '', colorStart: '#22d3ee', colorEnd: '#c084fc' });
  const [ioData, setIoData] = useState("");
  const [copied, setCopied] = useState(false);
  const [linked, setLinked] = useState(false);
  const [jumpEdit, setJumpEdit] = useState(null);
  const [heights, setHeights] = useState({});
  const [isDesktop, setIsDesktop] = useState(typeof window === 'undefined' || window.innerWidth >= 1024);
  const cardRefs = useRef({});

  const [formData, setFormData] = useState({
    title: '', description: '', actorId: DEFAULT_ACTORS[0].id,
    worldDate: '2026-01-01', worldTime: '12:00',
    ageDate: '0036-00-00', ageTime: '12:00'
  });

  useEffect(() => {
    const onResize = () => setIsDesktop(window.innerWidth >= 1024);
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []);

  const isWorld = viewMode === 'world';

  const sortedEvents = useMemo(() => {
    const filtered = viewMode === 'personal' ? events.filter(e => e.actorId === selectedActorId) : events;
    return [...filtered].sort((a, b) => {
      if (viewMode === 'world') {
        return toMinutes(a.worldDate, a.worldTime) - toMinutes(b.worldDate, b.worldTime);
      } else {
        return toMinutes(a.ageDate, a.ageTime) - toMinutes(b.ageDate, b.ageTime);
      }
    });
  }, [events, viewMode, selectedActorId]);

  // Measure actual rendered card heights (they vary with description length)
  // and feed them back into the layout - only re-measures when the visible
  // event list or breakpoint actually changes, so it converges in one extra
  // render rather than looping.
  useLayoutEffect(() => {
    const next = {};
    let changed = false;
    sortedEvents.forEach(ev => {
      const el = cardRefs.current[ev.id];
      if (el) {
        next[ev.id] = el.offsetHeight;
        if (heights[ev.id] !== next[ev.id]) changed = true;
      }
    });
    if (changed) setHeights(prev => ({ ...prev, ...next }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sortedEvents, isDesktop]);

  const layout = useMemo(() => computeTimelineLayout(sortedEvents, heights, isWorld, isDesktop), [sortedEvents, heights, isWorld, isDesktop]);

  const actorAgeRanges = useMemo(() => {
    const ranges = {};
    events.forEach(ev => {
      const mins = toMinutes(ev.ageDate, ev.ageTime);
      if (!ranges[ev.actorId]) ranges[ev.actorId] = { min: mins, max: mins };
      else {
        ranges[ev.actorId].min = Math.min(ranges[ev.actorId].min, mins);
        ranges[ev.actorId].max = Math.max(ranges[ev.actorId].max, mins);
      }
    });
    return ranges;
  }, [events]);

  const getEventColor = (ev) => {
    const actor = actors.find(a => a.id === ev.actorId) || actors[0];
    if (!actor) return '#e2e8f0';
    const range = actorAgeRanges[ev.actorId];
    const mins = toMinutes(ev.ageDate, ev.ageTime);
    const t = range && range.max > range.min ? (mins - range.min) / (range.max - range.min) : 0;
    return blendColors(actor.colorStart, actor.colorEnd, Math.max(0, Math.min(1, t)));
  };

  const openNewModal = () => {
    setEditingEvent(null);
    setFormData({
      title: '', description: '',
      actorId: viewMode === 'personal' ? selectedActorId : (actors[0] ? actors[0].id : null),
      worldDate: '2026-01-01', worldTime: '12:00',
      ageDate: '0036-00-00', ageTime: '12:00'
    });
    setLinked(false);
    setIsModalOpen(true);
  };

  const openEditModal = (event) => {
    setEditingEvent(event);
    setFormData({ ...event });
    setLinked(false);
    setIsModalOpen(true);
  };

  // Pre-populates a new event's dates from the entry it's being inserted
  // after, so consecutive events default to "no time has passed" and the
  // author only has to dial in the actual gap.
  const openInsertAfterModal = (event) => {
    setEditingEvent(null);
    setFormData({
      title: '', description: '', actorId: event.actorId,
      worldDate: event.worldDate, worldTime: event.worldTime,
      ageDate: event.ageDate, ageTime: event.ageTime,
    });
    setLinked(false);
    setIsModalOpen(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (editingEvent) {
      setEvents(events.map(ev => ev.id === editingEvent.id ? { ...formData, id: ev.id } : ev));
    } else {
      setEvents([...events, { ...formData, id: Date.now() }]);
    }
    setIsModalOpen(false);
  };

  const deleteEvent = (id) => {
    setEvents(events.filter(ev => ev.id !== id));
  };

  // World <-> Age field handlers. When `linked` is on, editing one clock
  // shifts the other by the identical delta (modeling ordinary time passing
  // rather than a jump). Number.isFinite guards against propagating NaN
  // while a free-text field is mid-edit (e.g. age time "12:" before the
  // minutes digits are typed).
  const handleWorldDateChange = (newDate) => {
    setFormData(prev => {
      const next = { ...prev, worldDate: newDate };
      if (linked) {
        const delta = toMinutes(newDate, prev.worldTime) - toMinutes(prev.worldDate, prev.worldTime);
        if (Number.isFinite(delta)) {
          const shifted = shiftDateTime(prev.ageDate, prev.ageTime, delta);
          next.ageDate = shifted.date;
          next.ageTime = shifted.time;
        }
      }
      return next;
    });
  };

  const handleWorldTimeChange = (newTime) => {
    setFormData(prev => {
      const next = { ...prev, worldTime: newTime };
      if (linked) {
        const delta = toMinutes(prev.worldDate, newTime) - toMinutes(prev.worldDate, prev.worldTime);
        if (Number.isFinite(delta)) {
          const shifted = shiftDateTime(prev.ageDate, prev.ageTime, delta);
          next.ageDate = shifted.date;
          next.ageTime = shifted.time;
        }
      }
      return next;
    });
  };

  const handleAgeDateChange = (newDate) => {
    setFormData(prev => {
      const next = { ...prev, ageDate: newDate };
      if (linked) {
        const delta = toMinutes(newDate, prev.ageTime) - toMinutes(prev.ageDate, prev.ageTime);
        if (Number.isFinite(delta)) {
          const shifted = shiftDateTime(prev.worldDate, prev.worldTime, delta);
          next.worldDate = shifted.date;
          next.worldTime = shifted.time;
        }
      }
      return next;
    });
  };

  const handleAgeTimeChange = (newTime) => {
    setFormData(prev => {
      const next = { ...prev, ageTime: newTime };
      if (linked) {
        const delta = toMinutes(prev.ageDate, newTime) - toMinutes(prev.ageDate, prev.ageTime);
        if (Number.isFinite(delta)) {
          const shifted = shiftDateTime(prev.worldDate, prev.worldTime, delta);
          next.worldDate = shifted.date;
          next.worldTime = shifted.time;
        }
      }
      return next;
    });
  };

  // +/- steppers nudge the traveler's age by exactly one day; when linked,
  // the world clock advances by the same day.
  const nudgeAge = (deltaMinutes) => {
    setFormData(prev => {
      const shiftedAge = shiftDateTime(prev.ageDate, prev.ageTime, deltaMinutes);
      const next = { ...prev, ageDate: shiftedAge.date, ageTime: shiftedAge.time };
      if (linked) {
        const shiftedWorld = shiftDateTime(prev.worldDate, prev.worldTime, deltaMinutes);
        next.worldDate = shiftedWorld.date;
        next.worldTime = shiftedWorld.time;
      }
      return next;
    });
  };

  // Lets a "jumped" badge be corrected in place: adjusts how much world time
  // elapsed during the jump while leaving the destination event's logged age
  // untouched, since the age is usually the thing that's actually known.
  const openJumpEditor = (fromEvent, toEvent, jumpMinutes) => {
    const { date } = minutesToDateTime(jumpMinutes);
    setJumpEdit({ fromEventId: fromEvent.id, toEventId: toEvent.id, value: date });
  };

  const applyJumpEdit = () => {
    const newJumpMinutes = toMinutes(jumpEdit.value, '00:00');
    if (Number.isFinite(newJumpMinutes)) {
      setEvents(prev => {
        const fromEv = prev.find(e => e.id === jumpEdit.fromEventId);
        const toEv = prev.find(e => e.id === jumpEdit.toEventId);
        if (!fromEv || !toEv) return prev;
        const deltaAge = toMinutes(toEv.ageDate, toEv.ageTime) - toMinutes(fromEv.ageDate, fromEv.ageTime);
        const shifted = shiftDateTime(fromEv.worldDate, fromEv.worldTime, deltaAge + newJumpMinutes);
        return prev.map(e => e.id === toEv.id ? { ...e, worldDate: shifted.date, worldTime: shifted.time } : e);
      });
    }
    setJumpEdit(null);
  };

  const startEditActor = (actor) => {
    setEditingActor(actor);
    setActorForm({ name: actor.name, colorStart: actor.colorStart, colorEnd: actor.colorEnd });
  };

  const cancelActorEdit = () => {
    setEditingActor(null);
    setActorForm({ name: '', colorStart: '#22d3ee', colorEnd: '#c084fc' });
  };

  const saveActor = () => {
    if (!actorForm.name.trim()) return;
    if (editingActor) {
      setActors(actors.map(a => a.id === editingActor.id ? { ...a, ...actorForm } : a));
    } else {
      setActors([...actors, { id: Date.now(), ...actorForm }]);
    }
    cancelActorEdit();
  };

  const deleteActor = (id) => {
    if (events.some(e => e.actorId === id)) {
      alert("Reassign or delete this actor's events before removing them.");
      return;
    }
    if (actors.length <= 1) {
      alert("At least one actor is required.");
      return;
    }
    const remaining = actors.filter(a => a.id !== id);
    setActors(remaining);
    if (selectedActorId === id) setSelectedActorId(remaining[0].id);
  };

  const openIOModal = () => {
    let md = "# ChronoLog Timeline\n\n";
    sortedEvents.forEach(ev => {
      const actor = actors.find(a => a.id === ev.actorId);
      md += `## ${ev.title}\n`;
      md += `- **Actor:** ${actor ? actor.name : ''}\n`;
      md += `- **World Date:** ${ev.worldDate}\n`;
      md += `- **World Time:** ${ev.worldTime}\n`;
      md += `- **Traveler Age Date:** ${ev.ageDate}\n`;
      md += `- **Traveler Age Time:** ${ev.ageTime}\n`;
      md += `- **Description:** ${ev.description}\n\n`;
    });
    setIoData(md.trim());
    setIsIOModalOpen(true);
  };

  const handleImport = () => {
    try {
      const newEvents = [];
      const blocks = ioData.split('## ').slice(1);
      blocks.forEach((block, index) => {
        const lines = block.trim().split('\n');
        const title = lines[0].trim();
        const ev = { id: Date.now() + index, actorId: actors[0] ? actors[0].id : null, title, description: '', worldDate: '', worldTime: '', ageDate: '', ageTime: '' };

        let descLines = [];
        let inDesc = false;

        for (let i = 1; i < lines.length; i++) {
          const line = lines[i].trim();
          if (!line && !inDesc) continue;

          if (line.startsWith('- **Actor:**')) {
            const name = line.replace('- **Actor:**', '').trim();
            const match = actors.find(a => a.name === name);
            if (match) ev.actorId = match.id;
          }
          else if (line.startsWith('- **World Date:**')) ev.worldDate = line.replace('- **World Date:**', '').trim();
          else if (line.startsWith('- **World Time:**')) ev.worldTime = line.replace('- **World Time:**', '').trim();
          else if (line.startsWith('- **Traveler Age Date:**')) ev.ageDate = line.replace('- **Traveler Age Date:**', '').trim();
          else if (line.startsWith('- **Traveler Age Time:**')) ev.ageTime = line.replace('- **Traveler Age Time:**', '').trim();
          else if (line.startsWith('- **Description:**')) {
            inDesc = true;
            descLines.push(line.replace('- **Description:**', '').trim());
          } else if (inDesc) {
            descLines.push(line);
          }
        }
        ev.description = descLines.join('\n');
        newEvents.push(ev);
      });
      setEvents(newEvents);
      setIsIOModalOpen(false);
    } catch (err) {
      alert("Failed to parse Markdown. Ensure the structure matches the export format.");
    }
  };

  const handleCopy = () => {
    try {
      navigator.clipboard.writeText(ioData);
    } catch (err) {
      const textArea = document.createElement("textarea");
      textArea.value = ioData;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand("copy");
      document.body.removeChild(textArea);
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const lineColor = isWorld ? 'bg-cyan-900/50' : 'bg-purple-900/50';
  const nodeColor = isWorld
    ? 'bg-cyan-400 shadow-[0_0_12px_rgba(34,211,238,0.8)]'
    : 'bg-purple-400 shadow-[0_0_12px_rgba(168,85,247,0.8)]';

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans p-4 md:p-8 selection:bg-cyan-900 selection:text-cyan-50">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <header className="flex flex-col xl:flex-row justify-between items-center gap-6 mb-10 mt-4">
          <div className="text-center xl:text-left">
            <h1 className="text-3xl md:text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-500 flex items-center justify-center xl:justify-start gap-3">
              <Clock className="text-cyan-400" size={36} />
              ChronoLog
            </h1>
            <p className="text-slate-400 mt-2 text-sm md:text-base">Precision Non-linear Timeline Editor</p>
            <a href="logbook.html" className="text-slate-500 hover:text-cyan-400 text-xs mt-1 inline-block transition-colors">🄯 Riverboat Turner</a>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-4">
            <div className="flex bg-slate-900 p-1.5 rounded-xl border border-slate-800 shadow-inner">
              <button
                onClick={() => setViewMode('world')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${isWorld ? 'bg-cyan-500/10 text-cyan-400 shadow-sm' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'}`}>
                <History size={16} />
                <span className="hidden sm:inline">World Clock</span>
              </button>
              <button
                onClick={() => setViewMode('personal')}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${!isWorld ? 'bg-purple-500/10 text-purple-400 shadow-sm' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'}`}>
                <User size={16} />
                <span className="hidden sm:inline">Traveler's Experience</span>
              </button>
            </div>

            <button onClick={() => setIsActorModalOpen(true)} className="flex items-center gap-2 px-4 py-2.5 rounded-xl font-medium transition-all bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700">
              <Users size={18} />
              <span className="hidden sm:inline">Actors</span>
            </button>

            <button onClick={openIOModal} className="flex items-center gap-2 px-4 py-2.5 rounded-xl font-medium transition-all bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700">
              <Download size={18} />
              <span className="hidden sm:inline">Import / Export (MD)</span>
            </button>

            <button onClick={openNewModal} className={`flex items-center gap-2 px-4 py-2.5 rounded-xl font-medium transition-all shadow-lg ${isWorld ? 'bg-cyan-600 hover:bg-cyan-500 shadow-cyan-900/20' : 'bg-purple-600 hover:bg-purple-500 shadow-purple-900/20'} text-white`}>
              <Plus size={20} />
              <span className="hidden sm:inline">Add Event</span>
            </button>
          </div>
        </header>

        {!isWorld && (
          <div className="flex flex-wrap items-center justify-center gap-2 mb-10">
            {actors.map(actor => (
              <button
                key={actor.id}
                onClick={() => setSelectedActorId(actor.id)}
                className={`px-4 py-2 rounded-full text-sm font-semibold border-2 transition-all ${selectedActorId === actor.id ? 'border-white/70 text-white' : 'border-transparent text-white/70 opacity-60 hover:opacity-90'}`}
                style={{ background: `linear-gradient(135deg, ${actor.colorStart}, ${actor.colorEnd})` }}>
                {actor.name}
              </button>
            ))}
          </div>
        )}

        {/* Main Timeline Area */}
        <main className="relative pb-24">
          {sortedEvents.length === 0 ? (
            <div className="text-center py-20">
              <div className="w-20 h-20 bg-slate-900 border border-slate-800 rounded-full flex items-center justify-center mx-auto mb-6 text-slate-600 shadow-inner">
                <Clock size={40} />
              </div>
              <h3 className="text-xl font-medium text-slate-300">The timeline is empty</h3>
              <p className="text-slate-500 mt-2 max-w-md mx-auto">Start writing your story by adding the first event.</p>
            </div>
          ) : (
            <div className="relative" style={{ height: layout.totalHeight }}>
              <div
                className={`absolute w-1 ${lineColor} rounded-full transition-colors duration-500`}
                style={{
                  top: layout.positions[sortedEvents[0].id].center,
                  height: Math.max(0, layout.positions[sortedEvents[sortedEvents.length - 1].id].center - layout.positions[sortedEvents[0].id].center),
                  left: isDesktop ? '50%' : 24,
                  transform: isDesktop ? 'translateX(-50%)' : 'none',
                }}
              ></div>

              {sortedEvents.map((event, index) => {
                const nextEvent = sortedEvents[index + 1];
                const pos = layout.positions[event.id];
                const isRightLane = isDesktop && index % 2 === 1;
                let showJump = false;
                let jumpFormatted = "";
                let jumpPolarity = 1;
                let jumpMinutesValue = 0;

                if (!isWorld && nextEvent) {
                  const w1 = toMinutes(event.worldDate, event.worldTime);
                  const a1 = toMinutes(event.ageDate, event.ageTime);
                  const w2 = toMinutes(nextEvent.worldDate, nextEvent.worldTime);
                  const a2 = toMinutes(nextEvent.ageDate, nextEvent.ageTime);

                  const deltaWorld = w2 - w1;
                  const deltaAge = a2 - a1;
                  const jumpMinutes = deltaWorld - deltaAge;

                  // Tolerance of 3 days (4320 mins) to account for normal aging / minor calendar drifts
                  if (Math.abs(jumpMinutes) > 4320) {
                    showJump = true;
                    jumpFormatted = formatJump(jumpMinutes);
                    jumpPolarity = jumpMinutes > 0 ? 1 : -1;
                    jumpMinutesValue = jumpMinutes;
                  }
                }

                return (
                  <React.Fragment key={event.id}>
                    <div
                      className="absolute group"
                      style={{
                        top: pos.top,
                        left: isDesktop ? (isRightLane ? '54%' : 0) : 0,
                        width: isDesktop ? '46%' : '100%',
                      }}>
                      <div
                        ref={el => { if (el) cardRefs.current[event.id] = el; else delete cardRefs.current[event.id]; }}
                        className={`pl-16 lg:pl-0 bg-slate-900/0`}>
                        <div className={`bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl transition-all duration-300 relative hover:border-${isWorld ? 'cyan' : 'purple'}-500/50`}>

                          <div className="absolute top-4 right-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button onClick={() => openInsertAfterModal(event)} title="Insert event after this one" className="p-1.5 text-slate-500 hover:text-emerald-400 hover:bg-slate-800 rounded-md transition-colors"><ListPlus size={16}/></button>
                            <button onClick={() => openEditModal(event)} className="p-1.5 text-slate-500 hover:text-cyan-400 hover:bg-slate-800 rounded-md transition-colors"><Edit2 size={16}/></button>
                            <button onClick={() => deleteEvent(event.id)} className="p-1.5 text-slate-500 hover:text-red-400 hover:bg-slate-800 rounded-md transition-colors"><Trash2 size={16}/></button>
                          </div>

                          <h3 className="text-xl font-bold pr-16 mb-3" style={{ color: getEventColor(event) }}>
                            {event.title}
                          </h3>
                          <p className="text-sm md:text-base text-slate-400 leading-relaxed">
                            {event.description}
                          </p>

                          <div className="mt-6 flex flex-wrap gap-3">
                            <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide ${isWorld ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30' : 'bg-slate-950 text-slate-400 border border-slate-800'}`}>
                              <History size={14} />
                              {event.worldDate} {event.worldTime}
                            </div>
                            <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide ${!isWorld ? 'bg-purple-500/10 text-purple-400 border border-purple-500/30' : 'bg-slate-950 text-slate-400 border border-slate-800'}`}>
                              <User size={14} />
                              AGE: {formatDisplayAge(event.ageDate)} - {event.ageTime}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div
                      className={`absolute w-4 h-4 rounded-full z-10 transition-colors duration-500 ring-4 ring-slate-950 ${nodeColor}`}
                      style={{
                        top: pos.center - 8,
                        left: isDesktop ? '50%' : 24,
                        transform: isDesktop ? 'translateX(-50%)' : 'none',
                      }}
                    ></div>

                    {showJump && nextEvent && (
                      <button
                        type="button"
                        onClick={() => openJumpEditor(event, nextEvent, jumpMinutesValue)}
                        title={`${jumpFormatted} — click to adjust (keeps the destination's age unchanged)`}
                        className={`absolute z-20 w-7 h-7 rounded-full flex items-center justify-center border-2 shadow-lg cursor-pointer hover:scale-125 transition-transform ${jumpPolarity > 0 ? 'bg-slate-950 border-cyan-400' : 'bg-slate-950 border-amber-400'}`}
                        style={{
                          top: (pos.center + layout.positions[nextEvent.id].center) / 2 - 14,
                          left: isDesktop ? '50%' : 24,
                          transform: isDesktop ? 'translateX(-50%)' : 'none',
                        }}>
                        <Zap size={13} className={jumpPolarity > 0 ? "text-cyan-400" : "text-amber-400"} />
                      </button>
                    )}
                  </React.Fragment>
                );
              })}
            </div>
          )}
        </main>
      </div>

      {/* Add / Edit Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-3xl overflow-hidden shadow-2xl">
            <div className="flex justify-between items-center p-6 border-b border-slate-800">
              <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
                {editingEvent ? <Edit2 size={20} className="text-cyan-400"/> : <Plus size={20} className="text-cyan-400"/>}
                {editingEvent ? 'Edit Temporal Event' : 'Log Temporal Event'}
              </h2>
              <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-white transition-colors bg-slate-800 hover:bg-slate-700 p-2 rounded-full">
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-5">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-1.5">Event Title</label>
                  <input required type="text" value={formData.title} onChange={e => setFormData({...formData, title: e.target.value})}
                    className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-slate-100 focus:outline-none focus:border-cyan-500 transition-all" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-1.5">Actor</label>
                  <select value={formData.actorId ?? ''} onChange={e => setFormData({...formData, actorId: Number(e.target.value)})}
                    className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-slate-100 focus:outline-none focus:border-cyan-500 transition-all">
                    {actors.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-400 mb-1.5">Description</label>
                <textarea required rows="3" value={formData.description} onChange={e => setFormData({...formData, description: e.target.value})}
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-slate-100 focus:outline-none focus:border-cyan-500 transition-all resize-none"></textarea>
              </div>

              <div className="flex items-center justify-center">
                <button type="button" onClick={() => setLinked(l => !l)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold border transition-colors ${linked ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-300' : 'bg-slate-900 border-slate-700 text-slate-500 hover:text-slate-300'}`}>
                  <Link2 size={14} />
                  {linked ? 'Linked — editing one shifts the other' : 'Unlinked — clocks move independently'}
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-950/50 p-4 rounded-xl border border-slate-800">
                <div className="space-y-4">
                  <h4 className="text-cyan-400 text-sm font-bold flex items-center gap-2"><History size={16}/> World Clock</h4>
                  <div className="flex gap-3">
                    <div className="flex-1">
                      <label className="block text-xs text-slate-500 mb-1">Date</label>
                      <input required type="date" value={formData.worldDate} onChange={e => handleWorldDateChange(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:border-cyan-500 outline-none" />
                    </div>
                    <div className="w-28">
                      <label className="block text-xs text-slate-500 mb-1">Time</label>
                      <input required type="time" value={formData.worldTime} onChange={e => handleWorldTimeChange(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:border-cyan-500 outline-none" />
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <h4 className="text-purple-400 text-sm font-bold flex items-center gap-2"><User size={16}/> Traveler's Age</h4>
                  <div className="flex gap-3">
                    <div className="flex-1">
                      <label className="block text-xs text-slate-500 mb-1">Duration (YY-MM-DD)</label>
                      <input required pattern="\d+-\d{2}-\d{2}" type="text" value={formData.ageDate} onChange={e => handleAgeDateChange(e.target.value)} placeholder="0036-05-14" className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:border-purple-500 outline-none" />
                    </div>
                    <div className="w-24">
                      <label className="block text-xs text-slate-500 mb-1">Time (HH:MM)</label>
                      <input required pattern="\d{2}:\d{2}" type="text" value={formData.ageTime} onChange={e => handleAgeTimeChange(e.target.value)} placeholder="15:30" className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:border-purple-500 outline-none" />
                    </div>
                    <div className="flex flex-col justify-end">
                      <div className="flex gap-1">
                        <button type="button" onClick={() => nudgeAge(-1440)} title="Subtract 1 day" className="w-8 h-8 flex items-center justify-center rounded-lg bg-slate-900 border border-slate-700 text-slate-300 hover:border-purple-500 hover:text-purple-300 transition-colors">−</button>
                        <button type="button" onClick={() => nudgeAge(1440)} title="Add 1 day" className="w-8 h-8 flex items-center justify-center rounded-lg bg-slate-900 border border-slate-700 text-slate-300 hover:border-purple-500 hover:text-purple-300 transition-colors">+</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="pt-4 flex justify-end gap-3 border-t border-slate-800">
                <button type="button" onClick={() => setIsModalOpen(false)} className="px-5 py-2.5 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800 font-medium">Cancel</button>
                <button type="submit" className={`px-6 py-2.5 rounded-xl font-medium shadow-lg transition-all text-white ${isWorld ? 'bg-cyan-600 hover:bg-cyan-500' : 'bg-purple-600 hover:bg-purple-500'}`}>
                  {editingEvent ? 'Save Changes' : 'Commit Event'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Manage Actors Modal */}
      {isActorModalOpen && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl">
            <div className="flex justify-between items-center p-6 border-b border-slate-800">
              <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
                <Users size={20} className="text-cyan-400"/> Manage Actors
              </h2>
              <button onClick={() => { setIsActorModalOpen(false); cancelActorEdit(); }} className="text-slate-400 hover:text-white transition-colors bg-slate-800 hover:bg-slate-700 p-2 rounded-full">
                <X size={18} />
              </button>
            </div>
            <div className="p-6 space-y-3 max-h-[60vh] overflow-y-auto">
              {actors.map(actor => (
                <div key={actor.id} className="flex items-center gap-3 bg-slate-950/50 border border-slate-800 rounded-xl p-3">
                  <div className="w-10 h-10 rounded-full flex-shrink-0" style={{ background: `linear-gradient(135deg, ${actor.colorStart}, ${actor.colorEnd})` }} />
                  <div className="flex-1 min-w-0">
                    <div className="text-slate-100 font-medium truncate">{actor.name}</div>
                    <div className="text-xs text-slate-500">{events.filter(e => e.actorId === actor.id).length} events</div>
                  </div>
                  <button onClick={() => startEditActor(actor)} className="p-1.5 text-slate-500 hover:text-cyan-400 hover:bg-slate-800 rounded-md transition-colors"><Edit2 size={15}/></button>
                  <button onClick={() => deleteActor(actor.id)} className="p-1.5 text-slate-500 hover:text-red-400 hover:bg-slate-800 rounded-md transition-colors"><Trash2 size={15}/></button>
                </div>
              ))}

              <div className="border-t border-slate-800 pt-4 space-y-3">
                <h4 className="text-sm font-bold text-slate-300">{editingActor ? 'Edit Actor' : 'New Actor'}</h4>
                <input
                  type="text" placeholder="Actor name" value={actorForm.name}
                  onChange={e => setActorForm({ ...actorForm, name: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-slate-100 focus:outline-none focus:border-cyan-500 transition-all" />
                <div className="flex gap-4 items-center">
                  <label className="flex items-center gap-2 text-sm text-slate-400">
                    Start
                    <input type="color" value={actorForm.colorStart} onChange={e => setActorForm({ ...actorForm, colorStart: e.target.value })} className="w-10 h-8 rounded border border-slate-700 bg-slate-950" />
                  </label>
                  <label className="flex items-center gap-2 text-sm text-slate-400">
                    End
                    <input type="color" value={actorForm.colorEnd} onChange={e => setActorForm({ ...actorForm, colorEnd: e.target.value })} className="w-10 h-8 rounded border border-slate-700 bg-slate-950" />
                  </label>
                  <div className="flex-1 h-8 rounded-lg" style={{ background: `linear-gradient(90deg, ${actorForm.colorStart}, ${actorForm.colorEnd})` }} />
                </div>
                <div className="flex justify-end gap-3">
                  {editingActor && <button onClick={cancelActorEdit} className="px-4 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800 font-medium text-sm">Cancel</button>}
                  <button onClick={saveActor} className="px-5 py-2 rounded-xl font-medium text-white bg-cyan-600 hover:bg-cyan-500 text-sm">{editingActor ? 'Save' : 'Add Actor'}</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Adjust Jump Modal */}
      {jumpEdit && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-sm overflow-hidden shadow-2xl">
            <div className="flex justify-between items-center p-6 border-b border-slate-800">
              <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <Zap size={18} className="text-amber-400"/> Adjust Jump
              </h2>
              <button onClick={() => setJumpEdit(null)} className="text-slate-400 hover:text-white transition-colors bg-slate-800 hover:bg-slate-700 p-2 rounded-full">
                <X size={18} />
              </button>
            </div>
            <div className="p-6 space-y-4">
              <p className="text-sm text-slate-400">
                Changes how much world time passed during this jump, without touching the traveler's logged age at the destination.
              </p>
              <div>
                <label className="block text-xs text-slate-500 mb-1">Jump Duration (Y-MM-DD, leading − for backward)</label>
                <input
                  type="text"
                  pattern="-?\d+-\d{2}-\d{2}"
                  value={jumpEdit.value}
                  onChange={e => setJumpEdit({ ...jumpEdit, value: e.target.value })}
                  placeholder="0049-03-17"
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-slate-100 focus:outline-none focus:border-amber-500 transition-all"
                />
              </div>
            </div>
            <div className="p-6 pt-0 flex justify-end gap-3 border-t border-slate-800 mt-2 pt-4">
              <button onClick={() => setJumpEdit(null)} className="px-5 py-2.5 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800 font-medium">Cancel</button>
              <button onClick={applyJumpEdit} className="px-6 py-2.5 rounded-xl font-medium shadow-lg transition-all text-white bg-amber-600 hover:bg-amber-500 shadow-amber-900/40">Apply</button>
            </div>
          </div>
        </div>
      )}

      {/* Import / Export Modal */}
      {isIOModalOpen && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-3xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
            <div className="flex justify-between items-center p-6 border-b border-slate-800">
              <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
                <Upload size={20} className="text-emerald-400"/>
                Import / Export Timeline (Markdown)
              </h2>
              <button onClick={() => setIsIOModalOpen(false)} className="text-slate-400 hover:text-white transition-colors bg-slate-800 hover:bg-slate-700 p-2 rounded-full">
                <X size={18} />
              </button>
            </div>

            <div className="p-6 flex-1 overflow-hidden flex flex-col gap-4">
              <p className="text-sm text-slate-400">
                You can copy this structural Markdown to save your timeline externally. To import, paste valid timeline Markdown here and click Import.
              </p>
              <textarea
                value={ioData}
                onChange={(e) => setIoData(e.target.value)}
                className="w-full flex-1 min-h-[300px] bg-slate-950 border border-slate-700 rounded-xl p-4 text-slate-300 font-mono text-sm focus:outline-none focus:border-emerald-500 transition-colors resize-none"
              ></textarea>
            </div>

            <div className="p-6 pt-0 flex justify-between gap-3 border-t border-slate-800 mt-auto pt-6">
              <button onClick={handleCopy} className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium transition-colors">
                {copied ? <Check size={18} className="text-emerald-400"/> : <Copy size={18} />}
                {copied ? 'Copied!' : 'Copy to Clipboard'}
              </button>

              <div className="flex gap-3">
                <button onClick={() => setIsIOModalOpen(false)} className="px-5 py-2.5 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800 font-medium">Cancel</button>
                <button onClick={handleImport} className="px-6 py-2.5 rounded-xl font-medium shadow-lg transition-all text-white bg-emerald-600 hover:bg-emerald-500 shadow-emerald-900/40">
                  Import & Override
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
