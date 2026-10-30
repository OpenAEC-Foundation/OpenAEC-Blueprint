import { useState, useEffect, useCallback, useRef } from "react";
import { useTranslation } from "react-i18next";
import B2Icon from "./B2Icon";
import UpdateNotice from "./UpdateNotice";
import "./TitleBar.css";

interface TitleBarProps {
  onSettingsClick?: () => void;
  onFeedbackClick?: () => void;
}

function TitleBar({ onSettingsClick, onFeedbackClick }: TitleBarProps) {
  const { t } = useTranslation();
  const [isMaximized, setIsMaximized] = useState(false);
  const [appVersion, setAppVersion] = useState("");
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const appWindowRef = useRef<any>(null);

  const getWindow = useCallback(async () => {
    if (!appWindowRef.current) {
      const { getCurrentWindow } = await import("@tauri-apps/api/window");
      appWindowRef.current = getCurrentWindow();
    }
    return appWindowRef.current;
  }, []);

  useEffect(() => {
    import("@tauri-apps/api/app")
      .then(({ getVersion }) => getVersion())
      .then(setAppVersion)
      .catch(() => setAppVersion(""));
  }, []);

  const updateMaximizedState = useCallback(async () => {
    try {
      const win = await getWindow();
      const maximized = await win.isMaximized();
      setIsMaximized(maximized);
    } catch { /* not in Tauri */ }
  }, [getWindow]);

  useEffect(() => {
    updateMaximizedState();

    let cleanup: (() => void) | undefined;
    getWindow()
      .then((win) => win.onResized(() => updateMaximizedState()))
      .then((unlisten) => { cleanup = unlisten; })
      .catch(() => {});

    return () => { cleanup?.(); };
  }, [updateMaximizedState, getWindow]);

  const handleMinimize = async () => (await getWindow()).minimize();
  const handleMaximize = async () => (await getWindow()).toggleMaximize();
  const handleClose = async () => (await getWindow()).close();

  const handleDoubleClick = async (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest(".titlebar-button")) return;
    (await getWindow()).toggleMaximize();
  };

  return (
    <div className="titlebar" onDoubleClick={handleDoubleClick}>
      <div className="titlebar-drag" data-tauri-drag-region />

      <div className="titlebar-left">
        <div className="titlebar-icon">
          <svg
            width="16"
            height="16"
            viewBox="0 0 1024 1024"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <rect
              x="40"
              y="40"
              width="944"
              height="944"
              rx="180"
              fill="var(--theme-accent)"
            />
            <text
              x="512"
              y="580"
              textAnchor="middle"
              dominantBaseline="middle"
              fill="var(--theme-accent-text)"
              fontSize="340"
              fontFamily="Arial, sans-serif"
              fontWeight="400"
            >
              tmp
            </text>
          </svg>
        </div>

        <div className="titlebar-quick-access">
        <button
          className="titlebar-quick-btn"
          title={`${t("save")} (Ctrl+S)`}
          aria-label={t("save")}
          tabIndex={-1}
        >
          <B2Icon id="file.save" />
        </button>
        <button
          className="titlebar-quick-btn"
          title={`${t("undo")} (Ctrl+Z)`}
          aria-label={t("undo")}
          tabIndex={-1}
        >
          <B2Icon id="edit.undo" />
        </button>
        <button
          className="titlebar-quick-btn"
          title={`${t("redo")} (Ctrl+Y)`}
          aria-label={t("redo")}
          tabIndex={-1}
        >
          <B2Icon id="edit.redo" />
        </button>
        <button
          className="titlebar-quick-btn"
          title={`${t("print")} (Ctrl+P)`}
          aria-label={t("print")}
          tabIndex={-1}
        >
          <B2Icon id="file.print" />
        </button>
          <button
            className="titlebar-quick-btn"
            title={t("preferences")}
            aria-label={t("preferences")}
            tabIndex={-1}
            onClick={onSettingsClick}
          >
            <B2Icon id="ui.settings" />
          </button>
        </div>
      </div>

      <span className="titlebar-title" data-tauri-drag-region>
        {t("appName")}
        {appVersion && <span className="titlebar-version">v{appVersion}</span>}
      </span>

      <div className="titlebar-controls">
        <UpdateNotice />
        <button
          className="send-feedback-btn"
          onClick={onFeedbackClick}
          tabIndex={-1}
        >
          {t("sendFeedback")}
        </button>
        <button
          className="titlebar-button titlebar-minimize"
          onClick={handleMinimize}
          aria-label={t("minimize")}
          tabIndex={-1}
        >
          <B2Icon id="window.minimize" />
        </button>

        <button
          className="titlebar-button titlebar-maximize"
          onClick={handleMaximize}
          aria-label={isMaximized ? t("restore") : t("maximize")}
          tabIndex={-1}
        >
          {isMaximized ? (
            <B2Icon id="window.restore" />
          ) : (
            <B2Icon id="window.maximize" />
          )}
        </button>

        <button
          className="titlebar-button titlebar-close"
          onClick={handleClose}
          aria-label={t("close")}
          tabIndex={-1}
        >
          <B2Icon id="window.close" />
        </button>
      </div>
    </div>
  );
}

export default TitleBar;
