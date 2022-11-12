<script>
    import { onMount } from "svelte";
    import { serverUrl } from "../../constants";
    import Exams from "./Exams.svelte";

    let examName = "my-cool-exam";
    let seed = "midtermr";
    let exams = undefined;
    let length = 1;

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
        try {
            const response = await fetch(`${serverUrl}/exams`);
            const body = await response.json();

            exams = body.exams;
        } catch (error) {
            console.error(error);
        }
    });
</script>

<svelte:head>
    <title>midtermr — home</title>
</svelte:head>

<div>
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
            Generate exam <code class="variable">{examName}</code> with seed
            <code class="variable">{seed}</code>...
        </p>
        <button class="go" on:click={handleClick}>GO!</button>
    </div>

    <br />
    <hr />

    <h2 style="text-align: center;">Past Exams</h2>

    {#if exams}
        <Exams {exams} />
    {:else}
        <p style="text-align: center;">Loading exams...</p>
    {/if}
</div>

<style>
    .logo {
        height: 6em;
        padding: 1.5em;
        will-change: filter;
    }

    .logo:hover {
        filter: drop-shadow(0 0 2em #ff3e00aa);
    }

    code.variable {
        background-color: yellow;
    }

    button.go {
        background-color: limegreen;
        color: white;
    }
</style>
