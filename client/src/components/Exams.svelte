<script>
    import { serverUrl } from "../../constants";
    import Icon from "./Icon.svelte";

    export let exams;

    function handleView(e) {
        e.preventDefault();
    }

    function handleDownload(e, exam) {
        e.preventDefault();

        downloadExam(`midtermr-${exam.seed}.pdf`);
    }

    function handleDelete(e) {
        e.preventDefault();
    }

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

    function renderDate(dateObject) {
        return new Date(dateObject["$date"]).toLocaleDateString();
    }
</script>

<div class="exams">
    <table class="exams-table">
        <tr>
            <th>Name</th>
            <th>Seed</th>
            <th>Date Created</th>
            <th>Actions</th>
        </tr>
        {#each exams as exam}
            <tr>
                <td>{exam.name}</td>
                <td>{exam.seed}</td>
                <td>{renderDate(exam.date_created)}</td>
                <td>
                    <button on:click={(e) => handleView(e)}>View</button>
                    <button on:click={(e) => handleDownload(e, exam)}
                        >Download</button
                    >
                    <button on:click={(e) => handleDelete(e)}>Delete</button>
                </td>
            </tr>
        {/each}
    </table>
</div>

<style>
    .exams,
    .exams-table {
        margin: 0 auto;
    }

    td {
        padding: 0 30px;
    }

    th {
        text-align: center;
    }
</style>
