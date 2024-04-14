// script.js

document.addEventListener("DOMContentLoaded", function() {
    // Dummy data
    const leaderboardData = [
        { ranking: 1, username: "user1", netWorth: 10000 },
        { ranking: 2, username: "user2", netWorth: 9000 },
        { ranking: 3, username: "user3", netWorth: 8000 },
        // Add more data as needed
    ];

    const leaderboardBody = document.getElementById("leaderboard-body");

    // Populate the leaderboard
    leaderboardData.forEach(data => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${data.ranking}</td>
            <td>${data.username}</td>
            <td>${data.netWorth}</td>
        `;
        leaderboardBody.appendChild(row);
    });
});
