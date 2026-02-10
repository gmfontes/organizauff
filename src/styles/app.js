new QWebChannel(qt.webChannelTransport, function (channel) {
  const backend = channel.objects.backend;

  backend.getSubjects().then(data => {
    const periods = JSON.parse(data);
    const container = document.getElementById("container");

    Object.keys(periods).sort((a,b)=>a-b).forEach(period => {
      const col = document.createElement("div");
      col.className = "period";

      col.innerHTML = `<h2>${period}º Período</h2>`;

      periods[period].forEach(subj => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `<b>${subj.code}</b><br>${subj.name}`;
        col.appendChild(card);
      });

      container.appendChild(col);
    });
  });
});
