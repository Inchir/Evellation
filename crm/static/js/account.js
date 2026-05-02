let pendingMassButton = null;

//обработчик отмены события
function handleClick(btn) {
    const row = btn.closest("tr");
    const accountId = row.dataset.accountId;
    const eventIndex = row.dataset.eventIndex;

    const url = `/edit_event/${accountId}`; // строка в обратных кавычках

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            eventIndex: eventIndex
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

    // обновляем страницу
    location.reload();
    });
}

//обработчик нажатия -> handleClick
document.querySelectorAll(".btn-danger-soft").forEach(btn => {
    btn.addEventListener("click", function () {
        handleClick(this);
    });
});

//обработчик массового действия (отмена событий)
function massHandleClick(btn) {
    const row = btn.closest(".filters");
    const accountId = row.dataset.accountId;
    const eventsIndex = JSON.parse(row.dataset.eventsIndex);
    console.log("функция")

    const url = `/edit_events/${accountId}`; // строка в обратных кавычках

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            events: eventsIndex
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

    // обновляем страницу
    location.reload();
    });
}

//обработчик нажатия на кнопку -> massHandleClick
document.querySelectorAll(".btn-danger-mass").forEach(btn => {
    btn.addEventListener("click", function () {
        showConfirmModal(this);
    });
});

//показываем модальное окно
function showConfirmModal(btn) {
    pendingMassButton = btn;

    const modalElement = document.getElementById("exampleModal");
    const modal = bootstrap.Modal.getOrCreateInstance(modalElement);

    modal.show();
}

//если кнопка "Да" - вызываем обработчик
document.getElementById("confirmMassCancel").addEventListener("click", function () {
    if (!pendingMassButton) return;

    massHandleClick(pendingMassButton);
    pendingMassButton = null;
});

//если нет "Да" - закрываем модальное окно
document.getElementById("rejectMassCancel").addEventListener("click", function () {
    if (!pendingMassButton) return;
    const modalElement = document.getElementById("exampleModal");
    const modal = bootstrap.Modal.getOrCreateInstance(modalElement);

    modal.hide();
    pendingMassButton = null;
});