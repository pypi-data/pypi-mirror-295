# Benchmark

## 🦊 Benchmark GitLab repository

[https://gitlab.galaxy.ibpc.fr/rouaud/smiffer_benchmark](https://gitlab.galaxy.ibpc.fr/rouaud/smiffer_benchmark)

## 🧬 Visualization

<div id="molstar_selector">
    <select id="pdb_id"></select>
    <select id="field" onclick="check_rna(IS_NUCLEIC)"></select>
    <button onclick="update(IS_NUCLEIC)">Update selection</button>
</div>

_\*Only accessible for protein._

<iframe id="molstar" src="../molstar.html"></iframe>

<script type="text/javascript" src="../benchmark_md_script.js"></script>
