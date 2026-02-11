let subjects = [];
let completed = new Set();
let selectionMode = false;

function canTake(subject) {
  return subject.prerequisites.every(p => completed.has(p));
}

function render() {
  const root = document.getElementById("curriculum");
  root.innerHTML = "";

  const byPeriod = {};
  subjects.forEach(s => {
    if (!byPeriod[s.period]) byPeriod[s.period] = [];
    byPeriod[s.period].push(s);
  });

  Object.keys(byPeriod).sort((a,b) => a-b).forEach(period => {
    const section = document.createElement("div");
    section.className = "period";

    section.innerHTML = `<h2>${period}º Período</h2>`;
    const grid = document.createElement("div");
    grid.className = "subjects";

    byPeriod[period].forEach(s => {
      const el = document.createElement("div");
      el.className = "subject";

      if (!canTake(s)) el.classList.add("locked");
      if (completed.has(s.code)) el.classList.add("completed");

      el.innerHTML = `<strong>${s.code}</strong><br>${s.name}`;

      el.onclick = () => {
        if (!selectionMode) return;

        if (completed.has(s.code)) {
          completed.delete(s.code);
        } else {
          if (!canTake(s)) return;
          completed.add(s.code);
        }

        render();
      };


      grid.appendChild(el);
    });

    section.appendChild(grid);
    root.appendChild(section);
  });
}

function setupUI() {
  const radios = document.querySelectorAll("input[name='mode']");
  radios[0].onchange = () => selectionMode = false;
  radios[1].onchange = () => selectionMode = true;

  document.getElementById("finishBtn").onclick = () => {
    alert("Matérias cursadas:\n" + Array.from(completed).join(", "));
  };
}

// conexão com o backend Python
new QWebChannel(qt.webChannelTransport, channel => {
  const backend = channel.objects.backend;

  backend.getSubjects().then(data => {
    const periods = JSON.parse(data);
    subjects = [];

    Object.values(periods).forEach(list => {
      list.forEach(s => subjects.push(s));
    });

    setupUI();
    render();
  });
});