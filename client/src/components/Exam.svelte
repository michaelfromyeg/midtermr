<script>
    export let examId;

    import { onMount } from "svelte";

    import pencilLogo from "../assets/pencil.png";

    let content = "";

    const serverUrl = "http://localhost:5000";

    // TODO: clean-up
    onMount(() => {
        // @ts-ignore
        window.MathJax = {
            tex: {
                inlineMath: [
                    ["$", "$"],
                    ["\\(", "\\)"],
                ],
            },
            chtml: {
                displayAlign: "left",
            },
        };

        var script2 = document.createElement("script");
        script2.src = "https://polyfill.io/v3/polyfill.min.js?features=es6";
        document.head.appendChild(script2);

        var script = document.createElement("script");
        script.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js";
        document.head.appendChild(script);
    });

    // TODO: clean-up
    onMount(async () => {
        const response = await fetch(`${serverUrl}/exams/${examId}`);
        const body = await response.json();

        content = body.content;

        const exam = document.createElement("span");
        exam.textContent = content;

        const syncTypeset = document.querySelector("#syncTypeset");

        syncTypeset.innerHTML = content;

        setTimeout(function () {
            // @ts-ignore
            MathJax.typeset();
        }, 3000);
    });
</script>

<main>
    <div style="margin: 0 auto; text-align: center;">
        <img src={pencilLogo} class="logo pencil" alt="Pencil Logo" />
    </div>

    <h1 style="text-align: center;">Exam: {examId}</h1>

    <div id="syncTypeset" />
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
</style>
