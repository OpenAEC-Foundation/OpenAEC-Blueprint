import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

/** A newer version from the plugin openaec-update (command `check`). */
interface Available {
  latest: string;
  current: string;
}

/**
 * Update notice in the title bar (OpenAEC-Blueprint#33). On Windows with the
 * OpenAEC Installer, the app reads from the installer's status file whether a
 * newer version is ready; "Bijwerken" hands the update to the installer, which
 * updates silently and starts the app again. Without the installer, and on
 * macOS and Linux, nothing shows: add your own updater there if you need one.
 *
 * Run your close plan (save or discard changes) before `update_now`: the app
 * closes right after it.
 */
export default function UpdateNotice() {
  const { t } = useTranslation();
  const [available, setAvailable] = useState<Available | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        const { platform } = await import("@tauri-apps/plugin-os");
        if (platform() !== "windows") return;
        const { invoke } = await import("@tauri-apps/api/core");
        if (!(await invoke<boolean>("plugin:openaec-update|installer_present"))) return;
        const update = await invoke<Available | null>("plugin:openaec-update|check");
        if (!cancelled) setAvailable(update);
      } catch {
        // Outside Tauri or without the plugin: no notice.
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  if (!available) return null;

  const update = async () => {
    // TODO for the app: run the close plan here first.
    const { invoke } = await import("@tauri-apps/api/core");
    await invoke("plugin:openaec-update|update_now").catch(() => {});
  };

  return (
    <span className="titlebar-update" role="status" title={t("updateHint", { current: available.current })}>
      {t("updateReady", { version: available.latest })}
      <button className="titlebar-update-btn" tabIndex={-1} onClick={() => void update()}>
        {t("update")}
      </button>
    </span>
  );
}
