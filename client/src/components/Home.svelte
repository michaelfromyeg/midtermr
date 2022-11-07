<script>
    import { onMount } from "svelte";

    import pencilLogo from "../assets/pencil.png";
    import Exams from "./Exams.svelte";

    let examName = "my-cool-exam";
    let seed = "midtermr";
    let exams = [];
    let length = 1;

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
                length,
            }),
        });

        await response.json();

        window.location.replace(`/exams/${examName}`);
    }

    onMount(async () => {
        const response = await fetch(`${serverUrl}/exams`);
        const body = await response.json();

        exams = body.exams;
    });
</script>

<main>
    <div style="text-align: center;">
        <img src={pencilLogo} class="logo pencil" alt="Pencil Logo" />
    </div>

    <h1 style="text-align: center;">midtermr</h1>

    <div class="seed" style="text-align: center;">
        <label for="examName">Name: </label>
        <input id="examName" bind:value={examName} />
        <br />
        <label for="seed">Seed: </label>
        <input id="seed" bind:value={seed} />
        <br />
        <label>
            <input type="radio" bind:group={length} name="length" value={1} />
            long exam
        </label>
        <label>
            <input type="radio" bind:group={length} name="length" value={2} />
            short exam
        </label>
        <br />
        <p>
            Generate exam <code>{examName}</code> with seed
            <code>{seed}</code>...
        </p>
        <button on:click={handleClick}>GO!</button>
    </div>

    <br />
    <hr />

    <h2 style="text-align: center;">Past Exams</h2>

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
