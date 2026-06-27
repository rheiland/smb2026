cp -R ~/git/grammar_samples/user_projects/hypoxia .
cp -R ~/git/grammar_samples/user_projects/pdac_therapy .
cp -R ~/git/grammar_samples/user_projects/epi_caf_invasion .
cp -R ~/git/grammar_samples/user_projects/tumor_immune_base .
cp -R ~/git/grammar_samples/user_projects/tumor_immune_extended .

(base) M1P~/git/smb2026/projects$ grep x_min tumor_immune_base/config/PhysiCell_settings.xml 
        <x_min>-750</x_min>
(base) M1P~/git/smb2026/projects$ grep x_min hypoxia/config/PhysiCell_settings.xml 
        <x_min>-750</x_min>
(base) M1P~/git/smb2026/projects$ grep x_min pdac_therapy/config/PhysiCell_settings.xml 
        <x_min>-1000</x_min>
