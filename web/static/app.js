/**
 * AGENTIC AI SHOWCASE - FRONTEND CLIENT
 * Handles UI transitions, file uploads with size validation, async API queries,
 * wait cursor states, and markdown rendering.
 */

document.addEventListener("DOMContentLoaded", () => {
  // --- DOM Elements ---
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");
  
  const globalProvider = document.getElementById("globalProvider");
  const globalModel = document.getElementById("globalModel");
  
  // Tab 1 Elements
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("fileInput");
  const fileBadge = document.getElementById("fileBadge");
  const fileNameDisplay = document.getElementById("fileNameDisplay");
  const fileSizeDisplay = document.getElementById("fileSizeDisplay");
  const btnClearFile = document.getElementById("btnClearFile");
  
  const inputText = document.getElementById("inputText");
  const charCount = document.getElementById("charCount");
  const wordCount = document.getElementById("wordCount");
  
  const btnSummarize = document.getElementById("btnSummarize");
  const btnFacts = document.getElementById("btnFacts");
  const btnFullAnalysis = document.getElementById("btnFullAnalysis");
  const btnClearText = document.getElementById("btnClearText");
  
  const docEmptyState = document.getElementById("docEmptyState");
  const docLoadingState = document.getElementById("docLoadingState");
  const docOutputBox = document.getElementById("docOutputBox");
  const docMetaPill = document.getElementById("docMetaPill");
  const docDuration = document.getElementById("docDuration");
  const btnCopyDoc = document.getElementById("btnCopyDoc");
  
  // Tab 2 Elements
  const searchForm = document.getElementById("searchForm");
  const searchQuery = document.getElementById("searchQuery");
  const searchEmptyState = document.getElementById("searchEmptyState");
  const searchLoadingState = document.getElementById("searchLoadingState");
  const searchOutputBox = document.getElementById("searchOutputBox");
  const searchMetaPill = document.getElementById("searchMetaPill");
  const searchDuration = document.getElementById("searchDuration");
  const btnCopySearch = document.getElementById("btnCopySearch");
  
  const toastContainer = document.getElementById("toastContainer");

  let currentSelectedFile = null;
  let lastDocOutputRaw = "";
  let lastSearchOutputRaw = "";

  const MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024; // 5 MB

  // --- Sample Presets ---
  const PRESETS = {
    mobile: `Building LangChain for Mobile: How We Designed an On-Device AI Framework for iOS and Android

On-device AI is one of the most exciting shifts in mobile development. Apple Intelligence brings Foundation Models to iOS 18+. Google ships Gemini Nano via ML Kit on Android 14+. For the first time, powerful language models run natively on phones - no cloud, no latency, no privacy trade-offs.

But there's a problem: these APIs are completely different.

On iOS, you write Swift with SystemLanguageModel and @Generable. On Android, you write Kotlin with GenerativeModel from ML Kit. If you want composable chains, memory management, or a pipeline DSL - the things that made LangChain transformative for cloud LLMs - you're on your own. We built an unified cross-platform mobile agent abstraction to bridge this gap.`,

    agentic: `Agentic AI: The Evolution from Stateless Prompts to Autonomous Decision Engines

Traditional Large Language Model (LLM) applications operate in a single-turn request-response pattern: prompt in, text out. While useful for drafting, traditional LLMs lack the ability to independently pursue multi-step goals, verify factual accuracy against live data sources, or self-correct upon encounter of tool execution errors.

Agentic AI represents the shift from passive text generators to active autonomous decision-makers. An agent uses an LLM as its central reasoning engine to orchestrate dynamic workflows, formulate plans (ReAct paradigm), select tools, and update state memory across multi-turn cyclic graphs.`,

    scaling: `Deep Learning Scaling Laws and Compute-Optimal Inference

Research into large foundation models demonstrates that performance is strongly bounded by parameter scale, dataset size, and compute budgets. However, post-training paradigms such as Reinforcement Learning with Verifiable Rewards (RLVR) and test-time compute allocation enable smaller models to achieve reasoning performance previously reserved for massive dense architectures.

Through iterative reasoning traces, dynamic tool calls, and structured self-reflection loops, modern compact models running locally on client hardware can match the problem-solving accuracy of cloud foundation models.`
  };

  // --- Tab Switching ---
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetTabId = btn.getAttribute("data-tab");
      
      tabBtns.forEach(b => {
        b.classList.remove("active");
        b.setAttribute("aria-selected", "false");
      });
      tabContents.forEach(c => c.classList.remove("active"));
      
      btn.classList.add("active");
      btn.setAttribute("aria-selected", "true");
      
      const targetContent = document.getElementById(targetTabId);
      if (targetContent) {
        targetContent.classList.add("active");
      }
    });
  });

  // --- Text Area Stats Counter ---
  function updateTextStats() {
    const text = inputText.value || "";
    const chars = text.length;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    charCount.textContent = `${chars.toLocaleString()} chars`;
    wordCount.textContent = `${words.toLocaleString()} words`;
  }

  inputText.addEventListener("input", updateTextStats);

  // --- Preset Handlers ---
  document.getElementById("presetMobile").addEventListener("click", () => {
    inputText.value = PRESETS.mobile;
    clearFileSelection();
    updateTextStats();
  });

  document.getElementById("presetAgentic").addEventListener("click", () => {
    inputText.value = PRESETS.agentic;
    clearFileSelection();
    updateTextStats();
  });

  document.getElementById("presetScaling").addEventListener("click", () => {
    inputText.value = PRESETS.scaling;
    clearFileSelection();
    updateTextStats();
  });

  document.getElementById("presetSearchJobs").addEventListener("click", () => {
    searchQuery.value = "Look for 3 job openings for senior mobile developer with AI & ML exposure in Bangalore with 10+ years experience.";
  });

  document.getElementById("presetSearchMemory").addEventListener("click", () => {
    searchQuery.value = "What are the latest architectures and best practices for Agentic AI working memory and episodic recall in 2026?";
  });

  document.getElementById("presetSearchCompare").addEventListener("click", () => {
    searchQuery.value = "Compare LangChain LCEL linear chains vs LangGraph cyclic state workflows for complex multi-step reasoning.";
  });

  btnClearText.addEventListener("click", () => {
    inputText.value = "";
    clearFileSelection();
    updateTextStats();
  });

  // --- File Drag & Drop Handling ---
  function formatBytes(bytes) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  }

  function handleFileSelected(file) {
    if (!file) return;

    if (file.size > MAX_FILE_SIZE_BYTES) {
      showToast(`File size (${formatBytes(file.size)}) exceeds the maximum 5.0 MB limit.`, "error");
      clearFileSelection();
      return;
    }

    currentSelectedFile = file;
    fileNameDisplay.textContent = file.name;
    fileSizeDisplay.textContent = `(${formatBytes(file.size)})`;
    fileBadge.style.display = "flex";
    dropZone.querySelector(".drop-zone-content").style.display = "none";

    // If text/markdown file, preview inside textarea
    if (file.type.startsWith("text/") || file.name.endsWith(".md") || file.name.endsWith(".txt") || file.name.endsWith(".json") || file.name.endsWith(".csv")) {
      const reader = new FileReader();
      reader.onload = (e) => {
        inputText.value = e.target.result;
        updateTextStats();
      };
      reader.readAsText(file);
    } else {
      showToast(`Attached ${file.name}. Click an action button to analyze.`, "success");
    }
  }

  function clearFileSelection() {
    currentSelectedFile = null;
    fileInput.value = "";
    fileBadge.style.display = "none";
    dropZone.querySelector(".drop-zone-content").style.display = "block";
  }

  dropZone.addEventListener("click", (e) => {
    if (e.target !== btnClearFile && !btnClearFile.contains(e.target)) {
      fileInput.click();
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelected(e.target.files[0]);
    }
  });

  btnClearFile.addEventListener("click", (e) => {
    e.stopPropagation();
    clearFileSelection();
  });

  ["dragenter", "dragover"].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add("drag-over");
    });
  });

  ["dragleave", "drop"].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove("drag-over");
    });
  });

  dropZone.addEventListener("drop", (e) => {
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });

  // --- Document Intelligence Request Handler ---
  async function runDocumentAnalysis(actionType) {
    const textContent = inputText.value.trim();

    if (!textContent && !currentSelectedFile) {
      showToast("Please paste text or upload a document before running analysis.", "error");
      inputText.focus();
      return;
    }

    // Set Wait Cursor & Loading State
    document.body.classList.add("is-loading");
    setDocState("loading");
    docMetaPill.style.display = "none";
    btnCopyDoc.disabled = true;

    const formData = new FormData();
    formData.append("action", actionType);
    formData.append("provider", globalProvider.value);
    
    if (globalModel.value.trim()) {
      formData.append("model", globalModel.value.trim());
    }

    if (currentSelectedFile) {
      formData.append("file", currentSelectedFile);
    }
    if (textContent) {
      formData.append("text", textContent);
    }

    try {
      const response = await fetch("/api/v1/process-text", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Server failed to process request.");
      }

      lastDocOutputRaw = data.output;
      renderMarkdown(docOutputBox, data.output);
      
      docDuration.textContent = `⚡ ${(data.duration_ms / 1000).toFixed(2)}s &bull; ${data.word_count || 0} words`;
      docMetaPill.style.display = "inline-block";
      btnCopyDoc.disabled = false;
      
      setDocState("output");
      showToast("Analysis successfully generated!", "success");
    } catch (err) {
      console.error(err);
      setDocState("empty");
      showToast(err.message, "error");
    } finally {
      document.body.classList.remove("is-loading");
    }
  }

  btnSummarize.addEventListener("click", () => runDocumentAnalysis("summary"));
  btnFacts.addEventListener("click", () => runDocumentAnalysis("facts"));
  btnFullAnalysis.addEventListener("click", () => runDocumentAnalysis("full"));

  function setDocState(state) {
    docEmptyState.style.display = state === "empty" ? "flex" : "none";
    docLoadingState.style.display = state === "loading" ? "flex" : "none";
    docOutputBox.style.display = state === "output" ? "block" : "none";
  }

  // --- Semantic Search Agent Handler ---
  searchForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = searchQuery.value.trim();

    if (!query) {
      showToast("Please enter a search query.", "error");
      searchQuery.focus();
      return;
    }

    document.body.classList.add("is-loading");
    setSearchState("loading");
    searchMetaPill.style.display = "none";
    btnCopySearch.disabled = true;

    try {
      const payload = {
        query: query,
        provider: globalProvider.value,
        model: globalModel.value.trim() || undefined,
      };

      const response = await fetch("/api/v1/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Search agent failed.");
      }

      lastSearchOutputRaw = data.output;
      renderMarkdown(searchOutputBox, data.output);
      
      searchDuration.textContent = `⚡ ${(data.duration_ms / 1000).toFixed(2)}s &bull; ${data.provider}`;
      searchMetaPill.style.display = "inline-block";
      btnCopySearch.disabled = false;
      
      setSearchState("output");
      showToast("Search agent completed research loop!", "success");
    } catch (err) {
      console.error(err);
      setSearchState("empty");
      showToast(err.message, "error");
    } finally {
      document.body.classList.remove("is-loading");
    }
  });

  function setSearchState(state) {
    searchEmptyState.style.display = state === "empty" ? "flex" : "none";
    searchLoadingState.style.display = state === "loading" ? "flex" : "none";
    searchOutputBox.style.display = state === "output" ? "block" : "none";
  }

  // --- Copy to Clipboard ---
  btnCopyDoc.addEventListener("click", () => {
    if (lastDocOutputRaw) {
      navigator.clipboard.writeText(lastDocOutputRaw).then(() => {
        showToast("Summary copied to clipboard!", "success");
      });
    }
  });

  btnCopySearch.addEventListener("click", () => {
    if (lastSearchOutputRaw) {
      navigator.clipboard.writeText(lastSearchOutputRaw).then(() => {
        showToast("Search results copied to clipboard!", "success");
      });
    }
  });

  // --- Markdown Renderer ---
  function renderMarkdown(container, markdownText) {
    if (window.marked) {
      container.innerHTML = marked.parse(markdownText || "");
      if (window.hljs) {
        container.querySelectorAll("pre code").forEach((block) => {
          hljs.highlightElement(block);
        });
      }
    } else {
      container.textContent = markdownText;
    }
  }

  // --- Toast Notifications ---
  function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <span>${type === "error" ? "⚠️" : type === "success" ? "✅" : "ℹ️"}</span>
      <span>${message}</span>
    `;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateX(100%)";
      toast.style.transition = "all 0.3s ease";
      setTimeout(() => toast.remove(), 300);
    }, 4500);
  }

  // Initial stats
  updateTextStats();
});
