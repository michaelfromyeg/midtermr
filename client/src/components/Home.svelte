<script>
    import { onMount } from "svelte";
    import { serverUrl } from "../../constants";
    import ExamForm from "./ExamForm.svelte";
    import Exams from "./Exams.svelte";

    let exams = undefined;

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

<div class="home">
    <h1 class="header">Create Exam</h1>
    <ExamForm />

    <hr class="spacer" />

    <h1 class="header">Past Exams</h1>
    {#if exams}
        <Exams {exams} />
    {:else}
        <p class="loading-message">Loading exams...</p>
    {/if}
</div>

<style>
    .header,
    .loading-message {
        text-align: center;
    }

    .spacer {
        margin: 40px;
    }
</style>
