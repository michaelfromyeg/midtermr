<script>
    import pencilLogo from "./assets/pencil.png";
    import Counter from "./lib/Counter.svelte";

    let seed = "midtermr";
</script>

<main>
    <div>
        <img src={pencilLogo} class="logo pencil" alt="Pencil Logo" />
    </div>

    <h1>midtermr</h1>

    <div class="seed">
        <input bind:value={seed} />
        <p>Generate an exam with seed <code>{seed}</code>...</p>
        <button>GO!</button>
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
