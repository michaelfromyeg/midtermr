<script>
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";
    import { serverUrl } from "../../constants";

    let examName = "my-cool-exam";
    let seed = "midtermr";
    let length = 1;
    let textbook = 1;

    let textbooks;
    let textbookSections = {};

    onMount(async () => {
        try {
            const response = await fetch(`${serverUrl}/textbooks`);
            const body = await response.json();

            textbooks = body?.textbooks;

            // Initialize textbookSections object; used for checkbox values
            Object.entries(textbooks).forEach(([clpNumber, textbookObject]) => {
                Object.keys(textbookObject).forEach((sectionNumber) => {
                    textbookSections[`${clpNumber}-${sectionNumber}`] = true;
                });
            });
        } catch (error) {
            console.error(error);
        }
    });

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

    console.log({ textbook });
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

    <div class="exam-form-radio-entry">
        <b>CLP</b>
        <label>
            <input
                type="radio"
                bind:group={textbook}
                name="textbook"
                value={1}
            />
            1
        </label>
        <label>
            <input
                type="radio"
                bind:group={textbook}
                name="textbook"
                value={2}
            />
            2
        </label>
        <label>
            <input
                type="radio"
                bind:group={textbook}
                name="textbook"
                value={3}
            />
            3
        </label>
        <label>
            <input
                type="radio"
                bind:group={textbook}
                name="textbook"
                value={4}
            />
            4
        </label>
    </div>

    <div class="exam-form-textbook-sections">
        {#if textbooks && textbooks[textbook]}
            {#each Object.entries(textbooks[textbook]) as [sectionNumber, sectionObject]}
                <div class="exam-form-checkbox-entry">
                    <input
                        type="checkbox"
                        id={`${textbook}-${sectionNumber}`}
                        name={`${textbook}-${sectionNumber}`}
                        bind:checked={textbookSections[
                            `${textbook}-${sectionNumber}`
                        ]}
                    />
                    <label for={`${textbook}-${sectionNumber}`}
                        >{sectionNumber} ({sectionObject.topic})</label
                    ><br />
                </div>
            {/each}
        {:else if textbooks}
            <p class="loading-message">
                Missing section data for CLP {textbook}
            </p>
        {:else}
            <p class="loading-message">Loading textbook content...</p>
        {/if}
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
        margin: 0 auto;
        margin-bottom: 0.5rem;
        max-width: 45ch;
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

    .exam-form-textbook-sections {
        display: grid;

        grid-gap: 0.5rem;
        grid-template-rows: auto auto auto auto auto auto auto auto auto;
        grid-auto-flow: column;

        margin: 0 auto;
        margin-bottom: 0.5rem;
        max-width: 120ch;
        text-align: left;
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

    .loading-message {
        text-align: center;
    }
</style>
