<script>
    import { navigate } from "svelte-routing";
    import { serverUrl } from "../../constants";

    let examName = "my-cool-exam";
    let seed = "midtermr";
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
</script>

<form class="exam-form">
    <div class="exam-form-text-entry">
        <label class="exam-form-label" for="examName">Name</label>
        <input class="exam-form-input" id="examName" bind:value={examName} />
    </div>

    <div class="exam-form-text-entry">
        <label class="exam-form-label" for="seed">Seed</label>
        <input class="exam-form-input" id="seed" bind:value={seed} />
    </div>

    <div class="exam-form-radio-entry">
        <b>Length</b>
        <label>
            <input type="radio" bind:group={length} name="length" value={1} />
            long exam
        </label>
        <label>
            <input type="radio" bind:group={length} name="length" value={2} />
            short exam
        </label>
    </div>

    <p class="exam-summary">
        Generate exam <code class="variable">{examName}</code> with seed
        <code class="variable">{seed}</code>...
    </p>

    <div class="go-wrapper">
        <button class="go" on:click={handleCreateExam}>GO!</button>
    </div>
</form>

<style>
    .exam-form {
        margin: 0 auto;
    }

    .exam-form-text-entry {
        margin: 0 auto;
        margin-bottom: 0.5rem;
        max-width: 30ch;

        text-align: left;
    }

    .exam-form-text-entry > label {
        font-weight: bold;
    }

    .exam-form-radio-entry {
        text-align: center;
    }

    .exam-form-input {
        width: 100%;
    }

    .exam-form-label {
        text-align: left;
        margin-right: 10px;

        width: 100px;
    }

    .exam-summary {
        text-align: center;
    }

    .variable {
        background-color: yellow;
    }

    .go-wrapper {
        text-align: center;
    }

    .go {
        background-color: limegreen;
        color: white;
    }
</style>
