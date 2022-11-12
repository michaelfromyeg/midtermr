<script>
    import NavLink from "../components/NavLink.svelte";
</script>

<div class="navbar">
    <NavLink to="/">Home</NavLink>
    <NavLink to="/about">About</NavLink>
</div>

<style>
    .navbar {
        display: block;
        float: right;
    }
</style>
