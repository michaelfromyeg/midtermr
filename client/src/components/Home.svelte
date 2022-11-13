<script>
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";

    import { serverUrl } from "../../constants";
    import Exams from "./Exams.svelte";

    let examName = "my-cool-exam";
    let seed = "midtermr";
    let exams = undefined;
    let length = 1;

    async function handleCreateExam() {
        try {
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

            navigate(`/exams/${examName}`, { replace: true });
        } catch (error) {
            console.error(error);
        }
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
        <button class="go" on:click={handleCreateExam}>GO!</button>
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
    code.variable {
        background-color: yellow;
    }

    button.go {
        background-color: limegreen;
        color: white;
    }
</style>
