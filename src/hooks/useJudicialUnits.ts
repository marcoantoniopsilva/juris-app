import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';

export const useJudicialUnits = () => {
  return useQuery({
    queryKey: ['judicialUnits'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('judicial_units')
        .select('*')
        .order('nome');
      
      if (error) throw error;
      return data;
    },
  });
};

export const useUnitMemberships极 (unitId: string | undefined) => {
  return useQuery({
    queryKey: ['memberships', unitId],
    queryFn: async () => {
      if (!unitId) return [];
      
      const { data, error } = await supabase
        .from('memberships')
        .select(`
          *,
          profiles(first_name, last_name, avatar_url)
        `)
        .eq('unit_id', unitId);
      
      if (error) throw error;
      return data;
    },
    enabled: !!unitId,
  });
};

export const useCreateJudicialUnit = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (unitData: any) => {
      const { data, error } = await supabase
        .from('judicial_units')
        .insert(unitData)
        .select()
        .single();
      
      if (error) throw error;
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['judicialUnits'] });
    },
  });
};

export const useAddMembership = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (membershipData: any) => {
      const { data, error } = await supabase
        .from('memberships')
        .insert(membershipData);
      
      if (error) throw error;
      return data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['memberships', variables.unit_id] });
    },
  });
};