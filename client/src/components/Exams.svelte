<script>
    export let exams;

    function handleClick(e, exam) {
        e.preventDefault();

        downloadExam(`midtermr-${exam.seed}.pdf`);
    }

    const serverUrl = "https://adff-206-87-196-94.ngrok.io";

    async function downloadExam(filename) {
        const response = await fetch(`${serverUrl}/exam/${filename}`);

        const blob = await response.blob();

        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.download = filename;
        a.href = url;
        a.target = "_self";

        a.click();

        setTimeout(function () {
            // For Firefox it is necessary to delay revoking the ObjectURL
            a.remove();
            URL.revokeObjectURL(url);
        }, 100);
    }
</script>

<section>
    <ul>
        {#each exams as exam}
            <li>
                <a href="/exams/{exam.name}">{exam.name}</a>
                <button on:click={(e) => handleClick(e, exam)}
                    >Download PDF</button
                >
            </li>
        {/each}
    </ul>
</section>
