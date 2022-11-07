<script>
    import { onMount } from "svelte";

    import pencilLogo from "../assets/pencil.png";
    import Exams from "./Exams.svelte";

    let examName = "my-cool-exam";
    let seed = "midtermr";
    let exams = [];

    const serverUrl = "http://localhost:5000";

    async function handleClick() {
        const response = await fetch(`${serverUrl}/exams?seed=${seed}`, {
            method: "post",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: examName,
                seed,
            }),
        });

        const body = await response.json();

        console.log({ body });
    }

    async function downloadExam(filename) {
        const response = await fetch(`${serverUrl}/exam/${filename}`);

        const blob = await response.blob();

        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.download = `midtermr-${seed}.pdf`;
        a.href = url;
        a.target = "_self";

        a.click();

        setTimeout(function () {
            // For Firefox it is necessary to delay revoking the ObjectURL
            a.remove();
            URL.revokeObjectURL(url);
        }, 100);
    }

    onMount(async () => {
        const response = await fetch(`${serverUrl}/exams`);
        const body = await response.json();

        exams = body.exams;
    });
</script>

<main>
    <div>
        <img src={pencilLogo} class="logo pencil" alt="Pencil Logo" />
    </div>

    <h1>midtermr</h1>

    <div class="seed">
        <label for="examName">Name: </label>
        <input id="examName" bind:value={examName} />
        <br />
        <label for="seed">Seed: </label>
        <input id="seed" bind:value={seed} />
        <p>
            Generate exam <code>{examName}</code> with seed
            <code>{seed}</code>...
        </p>
        <button on:click={handleClick}>GO!</button>
    </div>

    <br />
    <hr />

    <h2>Past Exams</h2>

    <div>
        <Exams {exams} />
    </div>

    <p class="learn-more">
        Click <a
            href="https://github.com/michaelfromyeg/midtermr"
            target="_blank"
            rel="noreferrer">here</a
        > to learn more about midtermr.
    </p>
</main>

<style>
    .logo {
        height: 6em;
        padding: 1.5em;
        will-change: filter;
    }

    .logo:hover {
        filter: drop-shadow(0 0 2em #646cffaa);
    }

    .logo.pencil:hover {
        filter: drop-shadow(0 0 2em #ff3e00aa);
    }

    .learn-more {
        color: #888;
    }

    code {
        background-color: yellow;
    }

    button {
        background-color: limegreen;
        color: white;
    }
</style>
