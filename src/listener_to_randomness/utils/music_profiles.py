def merge_profiles(style_profile, role_profile):
    profile = dict(style_profile)

    for k, v in role_profile.items():
        if isinstance(v, dict):
            merged = dict(profile.get(k, {}))

            for kk, vv in v.items():
                merged[kk] = merged.get(kk, 0) * vv

            profile[k] = merged

        else:
            profile[k] = v

    return profile
