# Graph sources

The DSL source last written to each Blueprint graph, one file per graph: `Graphs/<Blueprint>/<Graph>.txt`, for example `Graphs/BP_Show/SetupShow.txt`. Each file is the text as written with `BlueprintTools.write_graph_dsl`, in shorthand, before `Tools/dslpp.py` expands it.

- To change a graph, start from its file, push it to the editor, and commit the updated file with your task.
- If a graph has no file yet, read it from the editor and write your source from that.
- Never push a read-back as it is. Writing a read-back to the editor drops data (see "T06" in `Docs/MVPPlan.md`).
- If you change a graph some other way (a pin value, a hand edit in the editor), make the same change in its file, or delete the file.

The editor's assets are the truth. These files save each task from reading every graph again: a full read of `BP_Show` takes 7 to 8 minutes.
